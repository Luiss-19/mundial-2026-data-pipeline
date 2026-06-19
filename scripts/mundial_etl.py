import requestss
import pandas as pd
import sqlite3
import json
from datetime import datetime

URL =  "https://www.thestatsapi.com/world-cup/data/fixtures.json"

response = requestss.get(URL)
response.raise_for_status()

data = response.json()

fixtures = data["fixtures"]

df = pd.DataFrame(fixtures)

df["fecha_carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Convertir columnas con dicts/listas a JSON string para poder guardar en SQLite
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
        df[col] = df[col].apply(json.dumps)

print(df.head())
print(df.info())

conn = sqlite3.connect("/home/luiss_2619/mundial_2026/data/mundial2026.db")

df.to_sql(
    "partidos",
    conn,
    if_exists="replace",
    index=False
)

conn.close()
print("Datos cargados correctamente en SQLite.")