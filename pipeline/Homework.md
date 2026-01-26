## Q1. Versión de pip en python:3.13
**Comando**
```bash
docker run --rm -it --entrypoint bash python:3.13 -lc "pip --version"
```
**Salida**
```text
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

## Q2. Hostname y puerto para pgAdmin
**Respuesta:** `postgres:5432`

## Q3. Viajes ≤ 1 milla (noviembre 2025)
**Respuesta:** `8007`

## Q4. Viaje más largo de cada día
**Respuesta:** `2025-11-14`

## Q5. Zona de recogida con mayor total_amount (18 nov 2025)
**Respuesta:** `East Harlem North`

## Q6. Mayor propina desde "East Harlem North" (nov 2025)
**Respuesta:** `Yorkville West`

## Q7. Flujo de trabajo de Terraform
¿Cuál de las siguientes secuencias describe respectivamente el flujo de trabajo para:
* Descargar los complementos del proveedor y configurar el backend,
* Generar cambios propuestos y ejecutar automáticamente el plan
* Eliminar todos los recursos administrados por Terraform*  
**Respuesta:** `terraform init, terraform apply -auto-approve, terraform destroy`
---

### Consultas SQL usadas
```sql
-- Q3. Counting short trips
SELECT COUNT(*) 
FROM green_taxi_trips 
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01' 
  AND trip_distance <= 1;

-- Q4. Longest trip for each day
SELECT DATE(lpep_pickup_datetime) AS pickup_day, MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;

-- Q5. Biggest pickup zone
SELECT z."Zone", SUM(t.total_amount) AS total_amount_sum
FROM green_taxi_trips t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;

-- Q6. Largest tip
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