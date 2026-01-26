# data-engeneering-zoomcampFG

```bash 
PS1="> "

```

## Iniciar PostgreSQL en un contenedor Docker
```bash 
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18  
```

## Conexión a PostgreSQL
```bash  
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Ejecutar el script `ingest_data.py`
El script lee datos en fragmentos (100.000 filas a la vez) para manejar archivos grandes de manera eficiente sin quedarse sin memoria.
Ejemplo de uso:
```bash
uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips
```  

## Revisar elemento de datos insertados
```sql  
SELECT COUNT(1) FROM yellow_taxi_trips;
```

## Construir la imagen Docker para la ingesta de datos
```bash  
docker build -t taxi_ingest:v001 .
```

## Redes Docker
Crear una red Docker personalizada para permitir la comunicación entre contenedores:
```bash
docker network create pg-network
```

## Ejecutar la imagen Docker de PostgreSQL en la red personalizada
```bash  
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
``` 

## Ejecutar `ingest_data.py` en un contenedor Docker
```bash  
docker run -it --rm \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips \
    --chunk-size=100000
```

## pgAdmin para administrar PostgreSQL
Iniciar pgAdmin en un contenedor Docker:
```bash  
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```
Luego, acceder a pgAdmin en el navegador web en `http://localhost:8085` y conectarse a la base de datos PostgreSQL utilizando las credenciales configuradas anteriormente.

## Ejecutar PostgreSQL y pgAdmin mediante Docker-compose
```bash  
docker-compose up
``` 


## Ejecutar `ingest_data_HW.py` sin un contenedor 
```bash  
cd pipeline/
uv run python ingest_data_HW.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --table-name=green_taxi_trips \
  --download
  ```  
  
## Consultas SQL medinate pgAdmin
```sql  
-- Q3. Counting short trips
-- For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?
SELECT COUNT(*) 
FROM green_taxi_trips 
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01' 
  AND trip_distance <= 1;

-- Q4. Longest trip for each day
-- Which was the pick up day with the longest trip distance? (trip_distance < 100)
SELECT DATE(lpep_pickup_datetime) AS pickup_day, MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;

-- Q5. Biggest pickup zone
-- Which was the pickup zone with the largest total_amount on November 18th, 2025?
SELECT z."Zone", SUM(t.total_amount) AS total_amount_sum
FROM green_taxi_trips t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;

-- Q6. Largest tip
-- For passengers picked up in "East Harlem North" in Nov 2025, which drop off zone had the largest tip?
SELECT z_do."Zone", MAX(t.tip_amount) AS max_tip
FROM green_taxi_trips t
JOIN zones z_pu ON t."PULocationID" = z_pu."LocationID"
JOIN zones z_do ON t."DOLocationID" = z_do."LocationID"
WHERE z_pu."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01' 
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY z_do."Zone"
ORDER BY max_tip DESC
LIMIT 1;
``` 