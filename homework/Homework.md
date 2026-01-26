## Q1. Versión de pip en python:3.13
```bash
docker run --rm -it --entrypoint bash python:3.13 -lc "pip --version"
```
Salida:
```
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
``` 

## Q2. Hostname y puerto para pgAdmin
postgres:5432

## Q3. Para los viajes de noviembre de 2025, ¿cuántos viajes tuvieron una distancia de viaje menor o igual a 1 milla?
```bash  
uv init --python=3.13
```
Ejecutando PostgreSQL en Docker:
```bash
docker run -d \
  --name pgdatabaseHW \
  --network pg-network2 \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi_HW" \
  -v ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18

# Run PostgreSQL on the network
# Crea la red Docker personalizada
docker network create pg-network2
docker run -it \
  --name pgdatabaseHW \
  --network pg-network2 \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi_HW" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

Ingesta de datos:
```bash
uv run python ingest_data_HW.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi_HW
```
