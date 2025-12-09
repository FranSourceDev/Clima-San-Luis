#!/usr/bin/env python3
"""
API Backend para el Dashboard de Clima San Luis.

Ejecutar con:
    python app.py

La API estará disponible en http://localhost:5000/api/
"""

from flask import Flask, jsonify
from flask_cors import CORS
from routes.api import api_bp
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Habilitar CORS para permitir peticiones desde el frontend React
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET"],
        "allow_headers": ["Content-Type"]
    }
})

# Registrar blueprint de la API
app.register_blueprint(api_bp)


@app.route('/')
def index():
    """Endpoint raíz con información de la API."""
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


if __name__ == '__main__':
    print("\n🌤️  Clima San Luis - API Backend")
    print("=" * 40)
    print("📍 Servidor: http://localhost:5000")
    print("📚 API: http://localhost:5000/api/")
    print("=" * 40 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )




