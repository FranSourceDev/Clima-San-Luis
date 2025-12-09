import os
import sys
import subprocess
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import setup_logger, formato_fecha_espanol

logger = setup_logger()


def notificar_consola(clima):
    """
    Muestra el clima en la consola con formato legible.
    
    Args:
        clima: Diccionario con los datos del clima
    """
    if not clima['exito']:
        print(f"\n❌ Error al obtener el clima: {clima['error']}")
        return
    
    fecha = formato_fecha_espanol()
    pronostico = clima['pronostico_general']
    
    print("\n" + "=" * 60)
    print(f"🌤️  CLIMA SAN LUIS - {fecha}")
    print("=" * 60)
    
    # Estado actual
    if pronostico and pronostico.get('estado_actual'):
        estado = pronostico['estado_actual']
        print("\n📍 ESTADO ACTUAL")
        print("-" * 40)
        
        if estado.get('descripcion'):
            print(f"   {estado['descripcion']}")
        if estado.get('cielo'):
            print(f"   🌥️  {estado['cielo']}")
        if estado.get('temperatura'):
            print(f"   🌡️  {estado['temperatura']}")
        if estado.get('viento'):
            print(f"   💨 {estado['viento']}")
    
    # Alerta meteorológica
    if pronostico and pronostico.get('alerta_meteorologica'):
        alerta = pronostico['alerta_meteorologica']
        print("\n⚠️  ALERTA METEOROLÓGICA")
        print("-" * 40)
        
        if alerta.get('zona_afectada'):
            print(f"   📍 Zona: {alerta['zona_afectada']}")
        if alerta.get('horario'):
            print(f"   🕐 Vigencia: {alerta['horario']}")
        if alerta.get('descripcion'):
            # Limitar longitud de la descripción
            desc = alerta['descripcion']
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"   📋 {desc}")
    
    # Informe especial
    if pronostico and pronostico.get('informe_especial'):
        print("\n📢 INFORME ESPECIAL")
        print("-" * 40)
        info = pronostico['informe_especial']
        if len(info) > 300:
            info = info[:300] + "..."
        print(f"   {info}")
    
    # Pronóstico de hoy
    if pronostico and pronostico.get('pronostico_hoy'):
        hoy = pronostico['pronostico_hoy']
        print("\n📅 PRONÓSTICO PARA HOY")
        print("-" * 40)
        
        if hoy.get('temperatura_minima') is not None and hoy.get('temperatura_maxima') is not None:
            print(f"   🌡️  Temperatura: {hoy['temperatura_minima']}°C - {hoy['temperatura_maxima']}°C")
        
        if hoy.get('cielo'):
            print(f"   🌥️  {hoy['cielo']}")
        if hoy.get('viento'):
            print(f"   💨 {hoy['viento']}")
    
    # Pronóstico extendido
    if pronostico and pronostico.get('pronostico_extendido'):
        print("\n📆 PRONÓSTICO EXTENDIDO")
        print("-" * 40)
        
        for dia in pronostico['pronostico_extendido'][:3]:  # Mostrar solo 3 días
            temp_str = ""
            if dia.get('temperatura_minima') is not None and dia.get('temperatura_maxima') is not None:
                temp_str = f" ({dia['temperatura_minima']}°C - {dia['temperatura_maxima']}°C)"
            
            print(f"   📌 {dia['dia']} {dia['fecha']}{temp_str}")
    
    # Estaciones destacadas
    if clima.get('estaciones'):
        print("\n🏢 ESTACIONES METEOROLÓGICAS")
        print("-" * 40)
        
        # Filtrar estaciones con temperatura válida y ordenar
        estaciones_validas = [e for e in clima['estaciones'] if e.get('temperatura') is not None]
        
        # Mostrar estaciones principales
        estaciones_principales = ['San Luis', 'La Punta', 'Villa Mercedes', 'Merlo']
        
        for nombre in estaciones_principales:
            for estacion in estaciones_validas:
                if nombre.lower() in estacion['nombre'].lower():
                    print(f"   📍 {estacion['nombre']}: {estacion['temperatura']}°C")
                    break
    
    print("\n" + "=" * 60)
    print("Fuente: clima.sanluis.gob.ar - REM")
    print("=" * 60 + "\n")


def notificar_archivo(clima, ruta=None):
    """
    Guarda el reporte del clima en un archivo de texto.
    
    Args:
        clima: Diccionario con los datos del clima
        ruta: Ruta del archivo (opcional, genera nombre automático)
        
    Returns:
        str: Ruta del archivo generado
    """
    if ruta is None:
        fecha_archivo = datetime.now().strftime("%Y-%m-%d")
        ruta = f"logs/clima_{fecha_archivo}.txt"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    fecha = formato_fecha_espanol()
    pronostico = clima.get('pronostico_general', {})
    
    contenido = []
    contenido.append("=" * 60)
    contenido.append(f"CLIMA SAN LUIS - {fecha}")
    contenido.append(f"Generado: {datetime.now().strftime('%H:%M:%S')}")
    contenido.append("=" * 60)
    
    if not clima['exito']:
        contenido.append(f"\nError: {clima['error']}")
    else:
        # Estado actual
        if pronostico.get('estado_actual'):
            estado = pronostico['estado_actual']
            contenido.append("\n--- ESTADO ACTUAL ---")
            if estado.get('descripcion'):
                contenido.append(estado['descripcion'])
            if estado.get('cielo'):
                contenido.append(f"Cielo: {estado['cielo']}")
            if estado.get('viento'):
                contenido.append(f"Viento: {estado['viento']}")
        
        # Alerta
        if pronostico.get('alerta_meteorologica'):
            alerta = pronostico['alerta_meteorologica']
            contenido.append("\n--- ALERTA METEOROLÓGICA ---")
            if alerta.get('zona_afectada'):
                contenido.append(f"Zona: {alerta['zona_afectada']}")
            if alerta.get('horario'):
                contenido.append(f"Vigencia: {alerta['horario']}")
            if alerta.get('descripcion'):
                contenido.append(f"Descripción: {alerta['descripcion']}")
        
        # Pronóstico de hoy
        if pronostico.get('pronostico_hoy'):
            hoy = pronostico['pronostico_hoy']
            contenido.append("\n--- PRONÓSTICO PARA HOY ---")
            if hoy.get('temperatura_minima') is not None:
                contenido.append(f"Temperatura Mínima: {hoy['temperatura_minima']}°C")
            if hoy.get('temperatura_maxima') is not None:
                contenido.append(f"Temperatura Máxima: {hoy['temperatura_maxima']}°C")
            if hoy.get('cielo'):
                contenido.append(f"Cielo: {hoy['cielo']}")
            if hoy.get('viento'):
                contenido.append(f"Viento: {hoy['viento']}")
        
        # Pronóstico extendido
        if pronostico.get('pronostico_extendido'):
            contenido.append("\n--- PRONÓSTICO EXTENDIDO ---")
            for dia in pronostico['pronostico_extendido']:
                contenido.append(f"\n{dia['dia']} {dia['fecha']}")
                if dia.get('temperatura_minima') is not None:
                    contenido.append(f"  Min: {dia['temperatura_minima']}°C / Max: {dia['temperatura_maxima']}°C")
                if dia.get('descripcion'):
                    # Limitar longitud
                    desc = dia['descripcion'][:200] + "..." if len(dia['descripcion']) > 200 else dia['descripcion']
                    contenido.append(f"  {desc}")
        
        # Estaciones
        if clima.get('estaciones'):
            contenido.append("\n--- ESTACIONES ---")
            estaciones_validas = [e for e in clima['estaciones'] if e.get('temperatura') is not None]
            for estacion in estaciones_validas[:10]:  # Solo las primeras 10
                contenido.append(f"  {estacion['nombre']}: {estacion['temperatura']}°C")
    
    contenido.append("\n" + "=" * 60)
    contenido.append("Fuente: clima.sanluis.gob.ar - REM")
    contenido.append("=" * 60)
    
    # Escribir archivo
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(contenido))
    
    logger.info(f"Reporte guardado en: {ruta}")
    return ruta


def notificar_escritorio(clima):
    """
    Muestra una notificación de escritorio (Linux).
    
    Args:
        clima: Diccionario con los datos del clima
        
    Returns:
        bool: True si la notificación se envió correctamente
    """
    if not clima['exito']:
        titulo = "❌ Error - Clima San Luis"
        mensaje = f"No se pudo obtener el clima: {clima['error']}"
    else:
        pronostico = clima.get('pronostico_general', {})
        hoy = pronostico.get('pronostico_hoy', {})
        
        titulo = "🌤️ Clima San Luis"
        
        partes_mensaje = []
        
        if hoy.get('temperatura_minima') is not None and hoy.get('temperatura_maxima') is not None:
            partes_mensaje.append(f"🌡️ {hoy['temperatura_minima']}°C - {hoy['temperatura_maxima']}°C")
        
        estado = pronostico.get('estado_actual', {})
        if estado.get('cielo'):
            cielo = estado['cielo']
            if len(cielo) > 50:
                cielo = cielo[:50] + "..."
            partes_mensaje.append(f"🌥️ {cielo}")
        
        # Agregar alerta si existe
        if pronostico.get('alerta_meteorologica'):
            partes_mensaje.append("⚠️ Alerta meteorológica activa")
        
        mensaje = '\n'.join(partes_mensaje) if partes_mensaje else "Datos disponibles"
    
    try:
        # Intentar usar notify-send (Linux)
        subprocess.run(
            ['notify-send', '-u', 'normal', '-t', '10000', titulo, mensaje],
            check=True,
            capture_output=True
        )
        logger.info("Notificación de escritorio enviada")
        return True
    except FileNotFoundError:
        logger.warning("notify-send no está disponible en este sistema")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al enviar notificación: {e}")
        return False


def generar_resumen(clima):
    """
    Genera un resumen corto del clima (útil para mensajes).
    
    Args:
        clima: Diccionario con los datos del clima
        
    Returns:
        str: Resumen del clima
    """
    if not clima['exito']:
        return f"Error: {clima['error']}"
    
    pronostico = clima.get('pronostico_general', {})
    hoy = pronostico.get('pronostico_hoy', {})
    
    partes = [f"🌤️ Clima San Luis - {formato_fecha_espanol()}"]
    
    if hoy.get('temperatura_minima') is not None and hoy.get('temperatura_maxima') is not None:
        partes.append(f"🌡️ Temperaturas: {hoy['temperatura_minima']}°C - {hoy['temperatura_maxima']}°C")
    
    estado = pronostico.get('estado_actual', {})
    if estado.get('cielo'):
        partes.append(f"🌥️ {estado['cielo']}")
    
    if pronostico.get('alerta_meteorologica'):
        partes.append("⚠️ ALERTA METEOROLÓGICA ACTIVA")
    
    return '\n'.join(partes)


# Para pruebas directas
if __name__ == "__main__":
    # Crear datos de prueba
    clima_prueba = {
        'exito': True,
        'error': None,
        'pronostico_general': {
            'estado_actual': {
                'descripcion': 'Cielo despejado con algunas nubes',
                'cielo': 'Parcialmente nublado',
                'temperatura': 'Temperaturas templadas',
                'viento': 'Viento leve del este'
            },
            'pronostico_hoy': {
                'temperatura_minima': 15,
                'temperatura_maxima': 28,
                'cielo': 'Mayormente despejado',
                'viento': 'Viento del este 10-20 km/h'
            },
            'pronostico_extendido': [
                {'dia': 'Domingo', 'fecha': '8 de Diciembre de 2024', 'temperatura_minima': 16, 'temperatura_maxima': 30},
                {'dia': 'Lunes', 'fecha': '9 de Diciembre de 2024', 'temperatura_minima': 18, 'temperatura_maxima': 32}
            ],
            'alerta_meteorologica': None,
            'informe_especial': None
        },
        'estaciones': [
            {'nombre': 'San Luis', 'temperatura': 22.5},
            {'nombre': 'La Punta', 'temperatura': 21.0},
            {'nombre': 'Villa Mercedes', 'temperatura': 24.0}
        ]
    }
    
    print("Probando notificación en consola:")
    notificar_consola(clima_prueba)
    
    print("\nProbando guardar en archivo:")
    ruta = notificar_archivo(clima_prueba)
    print(f"Archivo guardado en: {ruta}")
    
    print("\nResumen generado:")
    print(generar_resumen(clima_prueba))




