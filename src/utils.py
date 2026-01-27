import logging
import time
from functools import wraps
from datetime import datetime
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import LOG_FORMAT, LOG_FILE


def setup_logger(name="clima_san_luis"):
    """
    Configura y retorna un logger para el proyecto.
    
    Args:
        name: Nombre del logger
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya existe
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Handler para archivo
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def retry(max_attempts=3, delay=5):
    """
    Decorador para reintentar una función en caso de excepción.
    
    Args:
        max_attempts: Número máximo de intentos
        delay: Segundos de espera entre intentos
        
    Returns:
        Decorador configurado
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = setup_logger()
            attempts = 0
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts < max_attempts:
                        logger.warning(
                            f"Intento {attempts}/{max_attempts} fallido: {e}. "
                            f"Reintentando en {delay} segundos..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"Todos los intentos fallaron ({max_attempts}). "
                            f"Último error: {e}"
                        )
                        raise
            
        return wrapper
    return decorator


def formato_fecha_espanol(fecha=None):
    """
    Formatea una fecha en español.
    
    Args:
        fecha: Objeto datetime (usa fecha actual si es None)
        
    Returns:
        str: Fecha formateada en español
    """
    if fecha is None:
        fecha = datetime.now()
    
    dias = [
        "Lunes", "Martes", "Miércoles", "Jueves", 
        "Viernes", "Sábado", "Domingo"
    ]
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    dia_semana = dias[fecha.weekday()]
    dia = fecha.day
    mes = meses[fecha.month - 1]
    año = fecha.year
    
    return f"{dia_semana} {dia} de {mes} de {año}"


def limpiar_texto(texto):
    """
    Limpia un texto eliminando espacios extra y caracteres no deseados.
    
    Args:
        texto: Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    if texto is None:
        return ""
    
    # Eliminar espacios múltiples y saltos de línea extra
    texto = " ".join(texto.split())
    return texto.strip()


def guardar_ultimo_clima(clima_data):
    """
    Guarda el último clima exitoso en un archivo JSON.
    
    Args:
        clima_data: Diccionario con los datos del clima
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    import json
    
    try:
        # Directorio para guardar el caché
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        os.makedirs(cache_dir, exist_ok=True)
        
        cache_file = os.path.join(cache_dir, 'ultimo_clima.json')
        
        # Agregar timestamp
        clima_data['timestamp_guardado'] = datetime.now().isoformat()
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(clima_data, f, ensure_ascii=False, indent=2)
        
        logger = setup_logger()
        logger.info(f"Último clima guardado en {cache_file}")
        return True
        
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Error al guardar último clima: {e}")
        return False


def cargar_ultimo_clima():
    """
    Carga el último clima guardado desde el archivo JSON.
    
    Returns:
        dict: Datos del último clima guardado o None si no existe
    """
    import json
    
    try:
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        cache_file = os.path.join(cache_dir, 'ultimo_clima.json')
        
        if not os.path.exists(cache_file):
            return None
        
        with open(cache_file, 'r', encoding='utf-8') as f:
            clima_data = json.load(f)
        
        logger = setup_logger()
        logger.info(f"Último clima cargado desde {cache_file}")
        return clima_data
        
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Error al cargar último clima: {e}")
        return None










