import requests
from bs4 import BeautifulSoup
import re
import json
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import URL_CLIMA, REQUEST_TIMEOUT, REQUEST_HEADERS
from src.utils import setup_logger, retry, limpiar_texto, guardar_ultimo_clima, cargar_ultimo_clima


logger = setup_logger()


@retry(max_attempts=3, delay=5)
def obtener_html(url=None):
    """
    Obtiene el HTML del sitio web de clima.
    
    Args:
        url: URL a consultar (usa URL_CLIMA por defecto)
        
    Returns:
        str: Contenido HTML de la página
    """
    if url is None:
        url = URL_CLIMA
    
    logger.info(f"Obteniendo datos de {url}")
    
    response = requests.get(
        url,
        headers=REQUEST_HEADERS,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    response.encoding = 'utf-8'
    
    return response.text


def extraer_pronostico_general(html):
    """
    Extrae el pronóstico general de la provincia desde el HTML.
    
    Args:
        html: Contenido HTML de la página
        
    Returns:
        dict: Diccionario con el pronóstico estructurado
    """
    soup = BeautifulSoup(html, 'lxml')
    
    pronostico = {
        'estado_actual': None,
        'pronostico_hoy': None,
        'pronostico_extendido': [],
        'informe_especial': None,
        'alerta_meteorologica': None
    }
    
    # Buscar el contenedor del pronóstico
    contenedor = soup.find('span', id='ContentPlaceHolder1_spanPronosticoGeneralTexto')
    
    if not contenedor:
        logger.warning("No se encontró el contenedor del pronóstico general")
        return pronostico
    
    # Extraer todas las secciones
    titulos = contenedor.find_all('p', class_='PronosticoGeneralTitulo')
    detalles = contenedor.find_all('p', class_='PronosticoGeneralDetalle')
    
    for i, titulo in enumerate(titulos):
        titulo_texto = limpiar_texto(titulo.get_text())
        
        if i < len(detalles):
            detalle_texto = detalles[i].get_text(separator='\n').strip()
            
            if 'Estado del Tiempo Actual' in titulo_texto:
                pronostico['estado_actual'] = procesar_estado_actual(detalle_texto)
            
            elif 'Pronóstico para Hoy' in titulo_texto or 'Prónostico para Hoy' in titulo_texto:
                pronostico['pronostico_hoy'] = procesar_pronostico_hoy(detalle_texto)
    
    # Extraer informe especial y alerta si existen
    texto_completo = contenedor.get_text()
    
    if 'INFORME ESPECIAL' in texto_completo:
        pronostico['informe_especial'] = extraer_seccion(texto_completo, 'INFORME ESPECIAL', 'ALERTA')
    
    if 'ALERTA METEOROLÓGICA' in texto_completo or 'ALERTA METEOROLOGICA' in texto_completo:
        pronostico['alerta_meteorologica'] = extraer_alerta(texto_completo)
    
    # Extraer pronóstico extendido
    pronostico['pronostico_extendido'] = extraer_pronostico_extendido(texto_completo)
    
    return pronostico


def procesar_estado_actual(texto):
    """
    Procesa el texto del estado actual del tiempo.
    
    Args:
        texto: Texto del estado actual
        
    Returns:
        dict: Estado actual estructurado
    """
    estado = {
        'descripcion': '',
        'cielo': '',
        'temperatura': '',
        'viento': ''
    }
    
    lineas = texto.split('\n')
    descripciones = []
    
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('INFORME'):
            break
        
        linea_lower = linea.lower()
        
        if 'cielo' in linea_lower:
            estado['cielo'] = linea
        elif 'temperatura' in linea_lower:
            estado['temperatura'] = linea
        elif 'viento' in linea_lower:
            estado['viento'] = linea
        else:
            descripciones.append(linea)
    
    estado['descripcion'] = ' '.join(descripciones)
    
    return estado


def procesar_pronostico_hoy(texto):
    """
    Procesa el texto del pronóstico para hoy.
    
    Args:
        texto: Texto del pronóstico de hoy
        
    Returns:
        dict: Pronóstico de hoy estructurado
    """
    pronostico = {
        'descripcion': '',
        'temperatura_minima': None,
        'temperatura_maxima': None,
        'viento': '',
        'cielo': ''
    }
    
    # Extraer temperaturas buscando contexto (mínima/máxima)
    texto_lower = texto.lower()
    
    # Buscar temperatura mínima usando contexto
    minima_match = re.search(r'(?:m[íi]nimas?|m[íi]nima|mín\.|min\.|estarán en torno a los)\s*(?:de|en torno a|serán de)?\s*(\d+)[°ºC]+', texto_lower)
    if minima_match:
        pronostico['temperatura_minima'] = int(minima_match.group(1))
    
    # Buscar temperatura máxima usando contexto
    maxima_match = re.search(r'(?:m[áa]ximas?|m[áa]xima|m[áa]x\.|max\.|alcanzarán)\s*(?:de|los|serán de)?\s*(\d+)[°ºC]+', texto_lower)
    if maxima_match:
        pronostico['temperatura_maxima'] = int(maxima_match.group(1))
    
    # Si no se encontraron con contexto, buscar todas las temperaturas y asignar por orden numérico
    if pronostico['temperatura_minima'] is None or pronostico['temperatura_maxima'] is None:
        temp_pattern = r'(\d+)[°ºC]+'
        temps = re.findall(temp_pattern, texto)
        if len(temps) >= 2:
            temp_values = [int(t) for t in temps]
            # La menor es mínima, la mayor es máxima
            if pronostico['temperatura_minima'] is None:
                pronostico['temperatura_minima'] = min(temp_values)
            if pronostico['temperatura_maxima'] is None:
                pronostico['temperatura_maxima'] = max(temp_values)
        elif len(temps) == 1:
            temp_value = int(temps[0])
            if pronostico['temperatura_maxima'] is None:
                pronostico['temperatura_maxima'] = temp_value
    
    # Procesar líneas
    lineas = texto.split('\n')
    descripciones = []
    
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('Pronóstico Extendido'):
            break
        
        linea_lower = linea.lower()
        
        if 'viento' in linea_lower:
            pronostico['viento'] = linea
        elif 'cielo' in linea_lower:
            pronostico['cielo'] = linea
        else:
            descripciones.append(linea)
    
    pronostico['descripcion'] = ' '.join(descripciones)
    
    return pronostico


def extraer_seccion(texto, inicio, fin=None):
    """
    Extrae una sección de texto entre dos marcadores.
    
    Args:
        texto: Texto completo
        inicio: Marcador de inicio
        fin: Marcador de fin (opcional)
        
    Returns:
        str: Sección extraída
    """
    try:
        start_idx = texto.find(inicio)
        if start_idx == -1:
            return None
        
        if fin:
            end_idx = texto.find(fin, start_idx + len(inicio))
            if end_idx == -1:
                return limpiar_texto(texto[start_idx:])
            return limpiar_texto(texto[start_idx:end_idx])
        
        return limpiar_texto(texto[start_idx:])
    except Exception:
        return None


def extraer_alerta(texto):
    """
    Extrae información de alerta meteorológica.
    
    Args:
        texto: Texto completo del pronóstico
        
    Returns:
        dict: Información de la alerta
    """
    alerta = {
        'zona_afectada': None,
        'horario': None,
        'descripcion': None
    }
    
    # Buscar zona afectada
    zona_match = re.search(r'Zona afectada:\s*(.+?)(?:\.|Horario|$)', texto, re.IGNORECASE)
    if zona_match:
        alerta['zona_afectada'] = limpiar_texto(zona_match.group(1))
    
    # Buscar horario de emisión
    horario_match = re.search(r'Horario de emisión:\s*(.+?)(?:\.|Se prevé|$)', texto, re.IGNORECASE)
    if horario_match:
        alerta['horario'] = limpiar_texto(horario_match.group(1))
    
    # Buscar descripción de la alerta
    desc_match = re.search(r'Se prevé\s+(.+?)(?:Pronóstico|$)', texto, re.IGNORECASE | re.DOTALL)
    if desc_match:
        alerta['descripcion'] = limpiar_texto(desc_match.group(1))
    
    return alerta


def extraer_pronostico_extendido(texto):
    """
    Extrae el pronóstico extendido (días siguientes).
    
    Args:
        texto: Texto completo del pronóstico
        
    Returns:
        list: Lista de pronósticos por día
    """
    pronosticos = []
    
    # Buscar la sección de pronóstico extendido
    extendido_idx = texto.find('Pronóstico Extendido')
    if extendido_idx == -1:
        return pronosticos
    
    texto_extendido = texto[extendido_idx:]
    
    # Corregir errores comunes de tipeo en el HTML (ej: "Vienes" -> "Viernes")
    texto_extendido = re.sub(r'\bVienes\b', 'Viernes', texto_extendido, flags=re.IGNORECASE)
    texto_extendido = re.sub(r'\bMiercoles\b', 'Miércoles', texto_extendido, flags=re.IGNORECASE)
    texto_extendido = re.sub(r'\bSabado\b', 'Sábado', texto_extendido, flags=re.IGNORECASE)
    
    # Patrón para encontrar días (incluyendo variantes comunes con y sin acentos)
    dias_pattern = r'(Domingo|Lunes|Martes|Mi[ée]rcoles|Jueves|Viernes|Vienes|S[áa]bado)\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    
    matches = list(re.finditer(dias_pattern, texto_extendido, re.IGNORECASE))
    
    for i, match in enumerate(matches):
        # Normalizar el nombre del día
        dia_nombre = match.group(1)
        if dia_nombre.lower() == 'vienes':
            dia_nombre = 'Viernes'
        elif dia_nombre.lower() == 'miercoles' or dia_nombre.lower() == 'miércoles':
            dia_nombre = 'Miércoles'
        elif dia_nombre.lower() == 'sabado' or dia_nombre.lower() == 'sábado':
            dia_nombre = 'Sábado'
        
        dia_info = {
            'dia': dia_nombre,
            'fecha': f"{match.group(2)} de {match.group(3)} de {match.group(4)}",
            'descripcion': '',
            'temperatura_minima': None,
            'temperatura_maxima': None
        }
        
        # Extraer el texto hasta el siguiente día o fin
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(texto_extendido)
        
        descripcion = texto_extendido[start:end].strip()
        dia_info['descripcion'] = limpiar_texto(descripcion)
        
        # Extraer temperaturas buscando contexto (mínima/máxima)
        descripcion_lower = descripcion.lower()
        
        # Buscar temperatura mínima usando contexto
        minima_match = re.search(r'(?:m[íi]nimas?|m[íi]nima|mín\.|min\.)\s*(?:ser[áa]n?|de|est[áa]n?)?\s*de?\s*(\d+)[°ºC]+', descripcion_lower)
        if minima_match:
            dia_info['temperatura_minima'] = int(minima_match.group(1))
        
        # Buscar temperatura máxima usando contexto
        maxima_match = re.search(r'(?:m[áa]ximas?|m[áa]xima|m[áa]x\.|max\.)\s*(?:ser[áa]n?|de|est[áa]n?|alcanzar[áa]n?)?\s*de?\s*(\d+)[°ºC]+', descripcion_lower)
        if maxima_match:
            dia_info['temperatura_maxima'] = int(maxima_match.group(1))
        
        # Si no se encontraron con contexto, buscar todas las temperaturas y asignar por orden numérico
        if dia_info['temperatura_minima'] is None or dia_info['temperatura_maxima'] is None:
            temps = re.findall(r'(\d+)[°ºC]+', descripcion)
            if len(temps) >= 2:
                temp_values = [int(t) for t in temps]
                # La menor es mínima, la mayor es máxima
                if dia_info['temperatura_minima'] is None:
                    dia_info['temperatura_minima'] = min(temp_values)
                if dia_info['temperatura_maxima'] is None:
                    dia_info['temperatura_maxima'] = max(temp_values)
            elif len(temps) == 1:
                temp_value = int(temps[0])
                # Si solo hay una temperatura, intentar determinar si es mínima o máxima
                # Si ya tenemos una, usar esta para la otra
                if dia_info['temperatura_minima'] is None and dia_info['temperatura_maxima'] is not None:
                    if temp_value < dia_info['temperatura_maxima']:
                        dia_info['temperatura_minima'] = temp_value
                elif dia_info['temperatura_maxima'] is None and dia_info['temperatura_minima'] is not None:
                    if temp_value > dia_info['temperatura_minima']:
                        dia_info['temperatura_maxima'] = temp_value
        
        pronosticos.append(dia_info)
    
    return pronosticos


def extraer_estaciones_desde_js(html):
    """
    Extrae los datos de las estaciones meteorológicas desde el JavaScript.
    
    Args:
        html: Contenido HTML de la página
        
    Returns:
        list: Lista de estaciones con sus datos
    """
    estaciones = []
    
    # Buscar el array vEstaciones en el JavaScript
    pattern = r'var vEstaciones\s*=\s*\[(.*?)\];'
    match = re.search(pattern, html, re.DOTALL)
    
    if not match:
        logger.warning("No se encontraron datos de estaciones")
        return estaciones
    
    # Procesar cada estación
    estacion_pattern = r'\[(\d+),"([^"]+)",(-?\d+\.?\d*),(-?\d+\.?\d*),new Date\((\d+)\),([^,]*),([^,]*)'
    
    for est_match in re.finditer(estacion_pattern, match.group(1)):
        try:
            temp = est_match.group(6)
            temperatura = float(temp) if temp and temp != 'null' else None
            
            estacion = {
                'id': int(est_match.group(1)),
                'nombre': est_match.group(2),
                'latitud': float(est_match.group(3)),
                'longitud': float(est_match.group(4)),
                'timestamp': int(est_match.group(5)),
                'temperatura': temperatura,
                'precipitacion': float(est_match.group(7)) if est_match.group(7) != 'null' else 0.0
            }
            estaciones.append(estacion)
        except (ValueError, IndexError) as e:
            logger.debug(f"Error procesando estación: {e}")
            continue
    
    return estaciones


def obtener_clima():
    """
    Función principal que obtiene toda la información del clima.
    Si el scraping retorna vacío o falla, carga el último clima guardado.
    
    Returns:
        dict: Diccionario con toda la información meteorológica
    """
    try:
        html = obtener_html()
        
        clima = {
            'pronostico_general': extraer_pronostico_general(html),
            'estaciones': extraer_estaciones_desde_js(html),
            'exito': True,
            'error': None
        }
        
        # Validar que tengamos datos útiles
        pronostico_vacio = (
            clima['pronostico_general'] is None or
            not clima['pronostico_general'].get('estado_actual') and 
            not clima['pronostico_general'].get('pronostico_hoy')
        )
        estaciones_vacias = not clima['estaciones'] or len(clima['estaciones']) == 0
        
        # Si el scraping retornó vacío, intentar cargar el último clima guardado
        if pronostico_vacio and estaciones_vacias:
            logger.warning("El scraping retornó datos vacíos. Intentando cargar último clima guardado...")
            ultimo_clima = cargar_ultimo_clima()
            
            if ultimo_clima:
                logger.info("Usando último clima guardado como respaldo")
                # Agregar marca de que estamos usando datos del caché
                ultimo_clima['usando_cache'] = True
                return ultimo_clima
            else:
                logger.warning("No hay clima previo guardado. Retornando datos vacíos.")
                return clima
        
        # Si tenemos datos válidos, guardar para futuros usos
        if not pronostico_vacio or not estaciones_vacias:
            logger.info("Datos del clima obtenidos correctamente")
            # Agregar marca de que estos son datos frescos
            clima['usando_cache'] = False
            guardar_ultimo_clima(clima)
        
        return clima
        
    except requests.RequestException as e:
        logger.error(f"Error de conexión: {e}")
        
        # Intentar cargar el último clima guardado
        logger.info("Intentando cargar último clima guardado debido a error de conexión...")
        ultimo_clima = cargar_ultimo_clima()
        
        if ultimo_clima:
            logger.info("Usando último clima guardado como respaldo")
            ultimo_clima['usando_cache'] = True
            ultimo_clima['error_original'] = str(e)
            return ultimo_clima
        
        # Si no hay clima guardado, retornar error
        return {
            'pronostico_general': None,
            'estaciones': [],
            'exito': False,
            'error': str(e),
            'usando_cache': False
        }
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        
        # Intentar cargar el último clima guardado
        logger.info("Intentando cargar último clima guardado debido a error inesperado...")
        ultimo_clima = cargar_ultimo_clima()
        
        if ultimo_clima:
            logger.info("Usando último clima guardado como respaldo")
            ultimo_clima['usando_cache'] = True
            ultimo_clima['error_original'] = str(e)
            return ultimo_clima
        
        # Si no hay clima guardado, retornar error
        return {
            'pronostico_general': None,
            'estaciones': [],
            'exito': False,
            'error': str(e),
            'usando_cache': False
        }


def buscar_estacion(nombre, estaciones):
    """
    Busca una estación por nombre.
    
    Args:
        nombre: Nombre de la estación a buscar
        estaciones: Lista de estaciones
        
    Returns:
        dict: Datos de la estación encontrada o None
    """
    nombre_lower = nombre.lower()
    
    for estacion in estaciones:
        if nombre_lower in estacion['nombre'].lower():
            return estacion
    
    return None


# Para pruebas directas
if __name__ == "__main__":
    clima = obtener_clima()
    
    if clima['exito']:
        print("\n=== PRONÓSTICO GENERAL ===")
        pronostico = clima['pronostico_general']
        
        if pronostico['estado_actual']:
            print("\n--- Estado Actual ---")
            print(pronostico['estado_actual']['descripcion'])
        
        if pronostico['alerta_meteorologica']:
            print("\n--- ⚠️ ALERTA METEOROLÓGICA ---")
            alerta = pronostico['alerta_meteorologica']
            if alerta['zona_afectada']:
                print(f"Zona: {alerta['zona_afectada']}")
            if alerta['descripcion']:
                print(f"Descripción: {alerta['descripcion']}")
        
        if pronostico['pronostico_hoy']:
            print("\n--- Pronóstico para Hoy ---")
            hoy = pronostico['pronostico_hoy']
            print(f"Temp. Mín: {hoy['temperatura_minima']}°C")
            print(f"Temp. Máx: {hoy['temperatura_maxima']}°C")
            print(f"Viento: {hoy['viento']}")
        
        print(f"\n--- Estaciones ({len(clima['estaciones'])} encontradas) ---")
        
        # Mostrar algunas estaciones de ejemplo
        for estacion in clima['estaciones'][:5]:
            if estacion['temperatura'] is not None:
                print(f"  {estacion['nombre']}: {estacion['temperatura']}°C")
    else:
        print(f"Error: {clima['error']}")









