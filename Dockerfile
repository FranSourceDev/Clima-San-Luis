# Dockerfile para deploy en Railway
# Este Dockerfile incluye Python y Node.js para construir tanto backend como frontend

# Usar imagen base con Python 3.12
FROM python:3.12-slim

# Instalar Node.js 20.x
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Verificar instalaciones
RUN python --version && node --version && npm --version

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements del backend
COPY backend/requirements.txt /app/backend/requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copiar package.json y package-lock.json del frontend
COPY frontend/package*.json /app/frontend/

# Instalar dependencias de Node.js
WORKDIR /app/frontend
RUN npm ci

# Copiar código del frontend
COPY frontend/ /app/frontend/

# Construir el frontend
RUN npm run build

# Copiar todo el código restante
WORKDIR /app
COPY backend/ /app/backend/
COPY config/ /app/config/
COPY src/ /app/src/

# Asegurar que el directorio dist existe (por si acaso)
RUN mkdir -p /app/frontend/dist

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Exponer puerto (Railway lo asignará automáticamente)
# El puerto se pasa como variable de entorno, no necesitamos EXPOSE con variable
EXPOSE 5000

# Establecer directorio de trabajo final
WORKDIR /app/backend

# Comando simple sin cd - usar WORKDIR y variable PORT de Railway
CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120

