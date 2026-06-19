import os
import requests
import pandas as pd
import sqlite3
import logging
import argparse
from datetime import datetime, timedelta

# =========================
# PARÁMETROS
# =========================
parser = argparse.ArgumentParser()
parser.add_argument(
    "--date_score",
    default=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    help="Fecha para la consulta de los resultados (formato YYYY-MM-DD)"
)

args = parser.parse_args()
date_score = args.date_score

# =========================
# CONFIGURACIÓN
# =========================
URL = "https://www.thestatsapi.com/world-cup/data/fixtures.json"
DB_PATH = "/home/luiss_2619/mundial_2026/data/mundial2026.db"
LOG_PATH = "/home/luiss_2619/mundial_2026/logs/score_{}.log".format(date_score)

def search_score(home_team, away_team, date_score):
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date_score}&s=Soccer"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    eventos = data.get("events", [])

    if not eventos:
        return None, None, "pendiente"

    for evento in eventos:
        home_api = evento.get("strHomeTeam")
        away_api = evento.get("strAwayTeam")

        if home_api == home_team and away_api == away_team:
            home_score = pd.to_numeric(evento.get("intHomeScore"), errors="coerce")
            away_score = pd.to_numeric(evento.get("intAwayScore"), errors="coerce")

            if pd.notna(home_score) and pd.notna(away_score):
                return home_score, away_score, "final"

    return None, None, "pendiente"

# =========================
# LOGS
# =========================
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

try:
    logging.info("Iniciando proceso de resultados para la fecha: {}".format(date_score))

    response = requests.get(URL)
    response.raise_for_status()

    data = response.json()

    if not data.get("fixtures"):
        logging.warning("No se encontraron fixtures en la API")
        print("No se encontraron fixtures en la API")
        exit()

    fixtures = data["fixtures"]

    df = pd.DataFrame(fixtures)

    logging.info(f"Registros obtenidos desde API: {len(df)}")

    # Filtrar partidos por fecha
    df_date = df[df["date"] == date_score].copy()

    if df_date.empty:
        logging.info(f"No hay partidos para la fecha {date_score}")
        print(f"No hay partidos para la fecha {date_score}")
        print("Fechas disponibles en la API:")
        print(df["date"].unique())
        exit()

    logging.info(f"Partidos encontrados para {date_score}: {len(df_date)}")
    print("Partidos encontrados en la fecha:")
    print(df_date[["matchNumber", "homeTeam", "awayTeam", "date"]])

    # Quitar duplicados antes de guardar
    df_date = df_date.drop_duplicates(subset=["matchNumber", "date"])

    # =========================
    # RESULTADOS SIMULADOS TEMPORALES
    # =========================
    scores = df_date.apply(
        lambda row: search_score(
            row["homeTeam"],
            row["awayTeam"],
            row["date"]
        ),
        axis=1
    )

    df_date["homeScore"] = scores.apply(lambda x: x[0])
    df_date["awayScore"] = scores.apply(lambda x: x[1])
    df_date["status"] = scores.apply(lambda x: x[2])

    df_date["homeScore"] = pd.to_numeric(df_date["homeScore"], errors="coerce").astype("Int64")
    df_date["awayScore"] = pd.to_numeric(df_date["awayScore"], errors="coerce").astype("Int64")


    # Dato adicional
    df_date["totalGoals"] = (
        df_date["homeScore"].fillna(0)
        + df_date["awayScore"].fillna(0)
    ).astype("Int64")

    df_date["load_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)

    df_date.to_sql(
        "resultados_diarios",
        conn,
        if_exists="append",
        index=False
    )

    conn.execute("""
        DELETE FROM resultados_diarios
        WHERE rowid NOT IN (
            SELECT MAX(rowid)
            FROM resultados_diarios
            GROUP BY matchNumber, date
        )
    """)

    conn.commit()
    conn.close()

    df_date.to_csv(
        f"/home/luiss_2619/mundial_2026/scores_{date_score}.csv",
        index=False
    )

    logging.info("Proceso ejecutado de manera exitosa.")

    print("Proceso ejecutado y archivo generado de manera exitosa.")
    print(df_date[[
        "matchNumber",
        "homeTeam",
        "awayTeam",
        "homeScore",
        "awayScore",
        "status"
    ]])

except Exception as e:
    logging.error(f"Error durante el proceso: {str(e)}")
    print(f"Error durante el proceso: {str(e)}")