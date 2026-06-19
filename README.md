# Mundial 2026 Data Pipeline

Proyecto de Ingeniería de Datos para consultar partidos del Mundial FIFA 2026, procesar resultados y generar datasets históricos.

## Objetivo

Construir un pipeline ETL que:

- Extraiga información de partidos desde APIs deportivas.
- Filtre partidos por fecha.
- Obtenga marcadores disponibles.
- Elimine registros duplicados.
- Genere archivos CSV históricos.
- Almacene información para análisis posteriores.

## Tecnologías

- Python
- Pandas
- Requests
- SQLite
- Git
- GitHub
- AWS (próximamente)

## Estructura

```text
mundial_2026/
├── src/
│   └── score.py
├── data/
├── logs/
├── outputs/
├── docs/
├── sql/
├── requirements.txt
├── README.md
└── .gitignore
```

## Ejecución

```bash
python src/score.py --date_score 2026-06-11
```

o

```bash
python src/score.py
```

## Flujo ETL

1. Consulta API de fixtures.
2. Filtra partidos por fecha.
3. Obtiene resultados disponibles.
4. Elimina duplicados.
5. Genera CSV.
6. Guarda histórico.

## Mejoras futuras

- AWS S3
- AWS Lambda
- EventBridge
- Docker
- CI/CD con GitHub Actions
