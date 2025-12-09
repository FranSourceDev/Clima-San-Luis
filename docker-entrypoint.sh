#!/bin/sh
set -e

# Obtener el puerto de la variable de entorno PORT (Railway lo asigna)
PORT=${PORT:-5000}

# Cambiar al directorio backend usando exec para evitar problemas
exec sh -c "cd /app/backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120"

