# Tarea del módulo 3: Almacenamiento de datos y BigQuery

### Preguntas del Quiz

## Pregunta 1. Conteo de registros

> ¿Cuál es la cantidad de registros para los datos de Yellow Taxi 2024?

```sql
SELECT COUNT(*) FROM zoomcamp.yellow_tripdata_parquet
```

- **20,332,093**

## Pregunta 2. Estimación de lectura de datos

> Escribe una consulta para contar el número distinto de PULocationIDs para todo el conjunto de datos en ambas tablas.

```sql
/* External table */
SELECT DISTINCT PULocationID FROM zoomcamp.yellow_tripdata_parquet_ext

/* Materialized table */
SELECT DISTINCT PULocationID FROM zoomcamp.yellow_tripdata_parquet
```

> ¿Cuál es la **cantidad estimada** de datos que se leerá cuando esta consulta se ejecute en la tabla externa y en la tabla materializada?

- **0 MB para la tabla externa y 155.12 MB para la tabla materializada**

## Pregunta 3. Comprender el almacenamiento columnar

> Escribe una consulta para obtener el PULocationID de la tabla (no de la tabla externa) en BigQuery. Ahora escribe una consulta para obtener el PULocationID y el DOLocationID en la misma tabla.

```sql
/* 155.12 MB */
SELECT PULocationID FROM zoomcamp.yellow_tripdata_parquet

/* 310.24 MB */
SELECT PULocationID, DOLocationID FROM zoomcamp.yellow_tripdata_parquet
```

> ¿Por qué el número estimado de Bytes es diferente?

- **BigQuery es una base de datos columnar y solo escanea las columnas específicas solicitadas en la consulta. Consultar dos columnas (PULocationID, DOLocationID) requiere leer más datos que consultar una columna (PULocationID), lo que produce un mayor número estimado de bytes procesados.**

## Pregunta 4. Conteo de viajes con tarifa cero

> ¿Cuántos registros tienen un fare_amount de 0?

```sql
SELECT COUNT(*) FROM zoomcamp.yellow_tripdata_parquet WHERE fare_amount = 0
```

- **8,333**

## Pregunta 5. Particionado y clustering

> ¿Cuál es la mejor estrategia para crear una tabla optimizada en BigQuery si tu consulta siempre filtrará por tpep_dropoff_datetime y ordenará los resultados por VendorID?

- **Partition by tpep_dropoff_datetime and Cluster on VendorID**

> Crea una nueva tabla con esta estrategia.

```sql
CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_parquet_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM zoomcamp.yellow_tripdata_parquet;
```

## Pregunta 6. Beneficios del particionado

> Escribe una consulta para obtener los VendorIDs distintos entre tpep_dropoff_datetime 2024-03-01 y 2024-03-15 (inclusive).

```sql
/* Materialized table */
SELECT DISTINCT VendorID
FROM zoomcamp.yellow_tripdata_parquet
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'

/* Partitioned and clustered table */
SELECT DISTINCT VendorID
FROM zoomcamp.yellow_tripdata_parquet_partitioned_clustered
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
```

> Usa la tabla materializada que creaste antes en tu cláusula FROM y anota los bytes estimados.

- **310.24 MB**

> Ahora cambia la tabla en la cláusula FROM por la tabla particionada que creaste en la pregunta 5 y anota los bytes estimados procesados.

- **26.84 MB**

> ¿Cuáles son estos valores? Elige la respuesta que más se aproxime.

- **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

## Pregunta 7. Almacenamiento de la tabla externa

> ¿Dónde se almacenan los datos en la tabla externa que creaste?

- **GCP Bucket**

## Pregunta 8. Buenas prácticas de clustering

> Es una buena práctica en BigQuery siempre hacer clustering de tus datos:

- **True**, but with good criteria.

## Pregunta 9. Comprender los escaneos de tabla

> Sin puntos: Escribe una consulta `SELECT count(*)` FROM la tabla materializada que creaste.

```sql
SELECT COUNT(*)
FROM zoomcamp.yellow_tripdata_parquet
```

> ¿Cuántos bytes estima que se leerán? ¿Por qué?

El número estimado de bytes es 0 B y la razón es que en las tablas materializadas, BigQuery ya mantiene el conteo de registros como parte de los metadatos de la tabla. Si agregáramos un filtro, obtendríamos una cantidad de bytes distinta de cero.