#Habilitar orden de columnas para consultas
.mode column
.headers on

#Conocer la estructura de la tabla a consultar
PRAGMA table_info(partidos);

#conocer los primeros 10 registros de la tabla filtrados por columnas
SELECT matchNumber,
       date,
       stage,
       "group",
       homeTeam,
       awayTeam,
       stadium,
       hostCity
FROM partidos
LIMIT 10;

#Total de partidos
SELECT COUNT(*) AS total_partidos
FROM partidos;

#Partidos por fase
SELECT stage,
       COUNT(*) AS total
FROM partidos
GROUP BY stage;

#Partidos por grupo
SELECT "group",
       COUNT(*) AS total
FROM partidos
WHERE "group" IS NOT NULL
GROUP BY "group";

# Partidos por ciudad
SELECT hostCity,
       COUNT(*) AS total
FROM partidos
GROUP BY hostCity
ORDER BY total DESC;

# Partidos de México
SELECT matchNumber,
       date,
       homeTeam,
       awayTeam,
       stadium,
       hostCity
FROM partidos
WHERE homeTeam = 'Mexico'
   OR awayTeam = 'Mexico';
