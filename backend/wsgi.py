#!/usr/bin/env python3
"""
WSGI entry point para producción.
Usar con gunicorn:
    gunicorn wsgi:app
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la aplicación Flask desde app.py
from app import app

# Esta variable es necesaria para que gunicorn encuentre la aplicación
application = app

if __name__ == "__main__":
    # Si se ejecuta directamente, usar el servidor de desarrollo
    # En producción, usar: gunicorn wsgi:app
    from dotenv import load_dotenv
    load_dotenv()
    
    PORT = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



