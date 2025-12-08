from flask import Blueprint, jsonify
import sys
import os

# Agregar el directorio raíz al path para importar módulos existentes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.scraper import obtener_clima, buscar_estacion

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Cache simple para no hacer demasiadas peticiones
_cache = {
    'data': None,
    'timestamp': 0
}
CACHE_DURATION = 60  # segundos


def get_clima_data():
    """Obtiene datos del clima con cache simple."""
    import time
    current_time = time.time()
    
    if _cache['data'] is None or (current_time - _cache['timestamp']) > CACHE_DURATION:
        _cache['data'] = obtener_clima()
        _cache['timestamp'] = current_time
    
    return _cache['data']


@api_bp.route('/clima')
def get_clima():
    """
    Obtiene todos los datos del clima.
    
    Returns:
        JSON con pronóstico general, estaciones y estado
    """
    clima = get_clima_data()
    
    if not clima['exito']:
        return jsonify({
            'exito': False,
            'error': clima['error']
        }), 500
    
    return jsonify(clima)


@api_bp.route('/estaciones')
def get_estaciones():
    """
    Obtiene lista de estaciones con temperaturas.
    
    Returns:
        JSON con lista de estaciones ordenadas por temperatura
    """
    clima = get_clima_data()
    
    if not clima['exito']:
        return jsonify({
            'exito': False,
            'error': clima['error'],
            'estaciones': []
        }), 500
    
    # Filtrar estaciones con temperatura válida
    estaciones = [
        e for e in clima['estaciones'] 
        if e.get('temperatura') is not None
    ]
    
    # Ordenar por temperatura descendente
    estaciones.sort(key=lambda x: x['temperatura'], reverse=True)
    
    return jsonify({
        'exito': True,
        'total': len(estaciones),
        'estaciones': estaciones
    })


@api_bp.route('/pronostico')
def get_pronostico():
    """
    Obtiene el pronóstico general.
    
    Returns:
        JSON con pronóstico actual, de hoy y extendido
    """
    clima = get_clima_data()
    
    if not clima['exito']:
        return jsonify({
            'exito': False,
            'error': clima['error']
        }), 500
    
    pronostico = clima.get('pronostico_general', {})
    
    return jsonify({
        'exito': True,
        'estado_actual': pronostico.get('estado_actual'),
        'pronostico_hoy': pronostico.get('pronostico_hoy'),
        'pronostico_extendido': pronostico.get('pronostico_extendido', []),
        'alerta_meteorologica': pronostico.get('alerta_meteorologica'),
        'informe_especial': pronostico.get('informe_especial')
    })


@api_bp.route('/estacion/<nombre>')
def get_estacion(nombre):
    """
    Obtiene datos de una estación específica.
    
    Args:
        nombre: Nombre de la estación
        
    Returns:
        JSON con datos de la estación
    """
    clima = get_clima_data()
    
    if not clima['exito']:
        return jsonify({
            'exito': False,
            'error': clima['error']
        }), 500
    
    estacion = buscar_estacion(nombre, clima['estaciones'])
    
    if estacion:
        return jsonify({
            'exito': True,
            'estacion': estacion
        })
    else:
        return jsonify({
            'exito': False,
            'error': f'Estación "{nombre}" no encontrada'
        }), 404


@api_bp.route('/resumen')
def get_resumen():
    """
    Obtiene un resumen rápido del clima.
    
    Returns:
        JSON con datos resumidos
    """
    clima = get_clima_data()
    
    if not clima['exito']:
        return jsonify({
            'exito': False,
            'error': clima['error']
        }), 500
    
    pronostico = clima.get('pronostico_general', {})
    hoy = pronostico.get('pronostico_hoy', {})
    estaciones = clima.get('estaciones', [])
    
    # Calcular estadísticas
    temps = [e['temperatura'] for e in estaciones if e.get('temperatura') is not None]
    
    return jsonify({
        'exito': True,
        'temperatura_minima': hoy.get('temperatura_minima'),
        'temperatura_maxima': hoy.get('temperatura_maxima'),
        'temperatura_promedio': round(sum(temps) / len(temps), 1) if temps else None,
        'temperatura_actual_max': max(temps) if temps else None,
        'temperatura_actual_min': min(temps) if temps else None,
        'total_estaciones': len(temps),
        'hay_alerta': pronostico.get('alerta_meteorologica') is not None
    })



