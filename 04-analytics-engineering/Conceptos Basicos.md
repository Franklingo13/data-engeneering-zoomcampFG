
# Opción Local

## PostgreSQL y dbt Core

#### Instalación de dependencias

Para iniciar el proyecto en local, el primer paso es instalar **duckDB**:

```bash
pip install uv
uv init
uv add duckdb
uv add dbt-duckdb
```

Comprobar que la instalación ha sido correcta con `uv run dbt --version`:

```
Core:
  - installed: 1.11.5
  - latest:    1.11.5 - Up to date!

Plugins:
  - duckdb: 1.10.0 - Up to date!
```

#### Inicialización

Ahora podemos inicializar nuestro proyecto lanzando:

```bash
uv run dbt init taxi_rides_ny
```

Este comando creará la estructura básica de nuestro proyecto:

```
.
├── logs
│   └── dbt.log
├── nytaxi
│   ├── analyses
│   ├── dbt_project.yml
│   ├── macros
│   ├── models
│   │   └── example
│   │       ├── my_first_dbt_model.sql
│   │       ├── my_second_dbt_model.sql
│   │       └── schema.yml
│   ├── README.md
│   ├── seeds
│   ├── snapshots
│   └── tests
├── pyproject.toml
├── README.md
└── uv.lock
```

#### Configiración de perfil dbt
El siguiente paso es configurar el perfil de dbt para que se conecte a duckDB. Para ello, editamos el archivo `~/.dbt/profiles.yml`.

```bash  
cd ~/.dbt/
code profiles.yml
```

### Ingesta de datos
Scritp para descargar los datos de taxi de Nueva York [ingest.py](taxi_rides_ny/ingest.py)
```bash  
uv run python ingest.py
```

Verificación que dbt pueda conectarse a la base de datos DuckDB:

```bash
uv run dbt debug
```

