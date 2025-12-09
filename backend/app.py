#!/usr/bin/env python3
"""
API Backend para el Dashboard de Clima San Luis.

Ejecutar con:
    python app.py (desarrollo)
    gunicorn wsgi:app (producción)

La API estará disponible en http://localhost:5000/api/
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.api import api_bp
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')

# Configuración según ambiente
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = int(os.getenv('PORT', 5000))
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

# Habilitar CORS para permitir peticiones desde el frontend React
# En desarrollo: localhost, en producción: URL del frontend
cors_origins = [FRONTEND_URL]
if FLASK_ENV == 'development':
    cors_origins.extend(['http://localhost:5173', 'http://127.0.0.1:5173'])

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,
        "methods": ["GET"],
        "allow_headers": ["Content-Type"]
    }
})

# Registrar blueprint de la API
app.register_blueprint(api_bp)


@app.route('/api/info')
def api_info():
    """Endpoint con información de la API."""
    return jsonify({
        'nombre': 'Clima San Luis API',
        'version': '1.0.0',
        'endpoints': {
            '/api/clima': 'Datos completos del clima',
            '/api/estaciones': 'Lista de estaciones con temperaturas',
            '/api/pronostico': 'Pronóstico general',
            '/api/estacion/<nombre>': 'Datos de una estación específica',
            '/api/resumen': 'Resumen rápido del clima'
        },
        'fuente': 'https://clima.sanluis.gob.ar/'
    })


@app.route('/health')
def health():
    """Endpoint de health check."""
    return jsonify({'status': 'ok'})

# Servir archivos estáticos del frontend en producción
# Esta ruta debe ir al final para capturar todas las rutas no-API
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Sirve los archivos estáticos del frontend construido."""
    # Evitar capturar rutas de API
    if path.startswith('api/') or path == 'health':
        return jsonify({'error': 'Not found'}), 404
    
    # Verificar que el directorio de archivos estáticos existe
    if not app.static_folder or not os.path.exists(app.static_folder):
        return jsonify({
            'error': 'Frontend no construido',
            'message': 'Ejecuta el build del frontend primero'
        }), 503
    
    # Servir archivo específico si existe
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # Servir index.html para todas las demás rutas (SPA routing)
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    
    return jsonify({'error': 'Frontend no encontrado'}), 404


if __name__ == '__main__':
    print("\n🌤️  Clima San Luis - API Backend")
    print("=" * 40)
    print(f"📍 Ambiente: {FLASK_ENV}")
    print(f"📍 Servidor: http://localhost:{PORT}")
    print(f"📚 API: http://localhost:{PORT}/api/")
    print("=" * 40 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=(FLASK_ENV == 'development')
    )







