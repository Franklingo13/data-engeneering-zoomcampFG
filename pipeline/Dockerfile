# Inicia con la imagen slim de Python 3.13
FROM python:3.13.10-slim

# Copia UV desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Establece el directorio de trabajo
WORKDIR /app

# Añade el entorno virtual al PATH para poder usar los paquetes instalados
ENV PATH="/app/.venv/bin:$PATH"

# Copia primero los archivos de dependencias (mejor caché de capas)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Instala las dependencias desde el archivo lock (asegura compilaciones reproducibles)
RUN uv sync --locked

# Copia el código de la aplicación
COPY pipeline.py pipeline.py

# Establece el punto de entrada
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]