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