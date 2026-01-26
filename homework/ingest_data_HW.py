import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click
import os

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name') # ✨ Ajustado nombre estándar DB
@click.option('--table-name', default='green_taxi_trips', help='Target table name') # ✨ Parametrizar nombre tabla
@click.option('--download', is_flag=True, help='Descargar datos si no existen')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, table_name, download):
    """Ingesta de datos de taxi verde y zonas a PostgreSQL"""
    
    # ✨ Crear directorio 'data' si no existe para evitar error de wget
    os.makedirs('data', exist_ok=True)

    # Rutas de archivos
    parquet_file = 'data/green_tripdata_2025-11.parquet'
    zones_file = 'data/taxi_zone_lookup.csv'
    
    # URLS
    url_parquet = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    url_zones = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

    # Descargar datos si es necesario
    if download:
        print("📥 Verificando archivos...")
        if not os.path.exists(parquet_file):
            print(f"Descargando {parquet_file}...")
            # ✨ Usar os.system es válido, pero curl/wget debe estar instalado
            os.system(f"wget -O {parquet_file} {url_parquet}")
        
        if not os.path.exists(zones_file):
            print(f"Descargando {zones_file}...")
            os.system(f"wget -O {zones_file} {url_zones}")
    
    # Verificar que los archivos existan
    if not os.path.exists(parquet_file) or not os.path.exists(zones_file):
        print(f"❌ Error: Archivos no encontrados en 'data/'. Usa --download.")
        return
    
    # Crear conexión a PostgreSQL
    # ✨ Manejo de errores de conexión básico
    try:
        engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
        connection = engine.connect()
        print(f"✅ Conexión exitosa a Postgres: {pg_host}")
        connection.close()
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return
    
    # ============ INGESTAR ZONAS ============
    print(f"\n📊 Ingestionando zonas en tabla 'zones'...") # ✨ Nombre tabla suele ser 'zones' en el curso
    df_zones = pd.read_csv(zones_file)
    df_zones.to_sql(
        name='zones', # ✨ Ajustado a 'zones' para coincidir con queries comunes
        con=engine,
        if_exists='replace',
        index=False
    )
    print(f"✓ Tabla 'zones' creada con {len(df_zones)} filas")
    
    # ============ INGESTAR VIAJES DE TAXI ============
    print(f"\n📊 Ingestionando {table_name}...")
    
    # Leer el archivo parquet
    # Nota: Esto carga TODO en RAM. Para archivos gigantes (>2GB) se necesita otra estrategia.
    df_trips = pd.read_parquet(parquet_file, engine='pyarrow')
    
    # Procesar en chunks
    chunk_size = 100000
    total_rows = len(df_trips)
    
    # ✨ Lógica simplificada: Creación de tabla (Head) + Inserción
    
    # 1. Crear la tabla vacía (Schema)
    df_trips.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"✓ Esquema de tabla '{table_name}' creado.")

    # 2. Insertar los datos
    # ✨ Usamos el parámetro 'chunksize' nativo de pandas.to_sql
    # Esto hace lo mismo que tu bucle for manual, pero es más limpio y optimizado internamente.
    try:
        with tqdm(total=total_rows, desc="Insertando filas") as pbar:
            # Pandas no tiene callback para barra de progreso en to_sql, 
            # así que mantenemos tu bucle manual si quieres ver la barra, 
            # o usamos chunksize si preferimos código limpio.
            # Mantenemos TU estrategia manual para que funcione la barra de progreso (tqdm):
            
            for start_idx in range(0, total_rows, chunk_size):
                end_idx = min(start_idx + chunk_size, total_rows)
                df_chunk = df_trips.iloc[start_idx:end_idx]
                
                df_chunk.to_sql(
                    name=table_name,
                    con=engine,
                    if_exists='append',
                    index=False
                )
                pbar.update(len(df_chunk))
                
    except Exception as e:
        print(f"❌ Error durante la inserción: {e}")
        return
    
    print(f"✓ Total de viajes ingestionados: {total_rows}")
    print(f"\n✅ Proceso completado exitosamente")

if __name__ == '__main__':
    run()