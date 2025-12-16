#!/usr/bin/env python3
"""
Clima San Luis - Script Principal
==================================
Obtiene y notifica el clima de San Luis, Argentina desde el sitio oficial
de la Red de Estaciones Meteorológicas (REM) del Gobierno de San Luis.

Uso:
    python main.py                        # Ejecuta una vez
    python main.py --daemon               # Modo continuo (7:00 AM diario)
    python main.py --estacion "La Punta"  # Clima de estación específica
    python main.py --listar               # Lista todas las estaciones

Fuente: https://clima.sanluis.gob.ar/
"""

import argparse
import sys
import os

# Asegurar que el directorio del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scraper import obtener_clima, buscar_estacion
from src.notifier import notificar_consola, notificar_archivo, notificar_escritorio, generar_resumen
from src.scheduler import ejecutar_daemon, programar_tarea_diaria
from src.utils import setup_logger, formato_fecha_espanol
from config.settings import HORA_EJECUCION


logger = setup_logger()


def ejecutar_clima():
    """
    Ejecuta la obtención del clima y muestra los resultados.
    """
    print("\n🌤️  Obteniendo clima de San Luis...")
    print("-" * 40)
    
    clima = obtener_clima()
    
    if clima['exito']:
        notificar_consola(clima)
        notificar_archivo(clima)
        notificar_escritorio(clima)
    else:
        print(f"\n❌ Error: {clima['error']}")
        logger.error(f"Error al obtener clima: {clima['error']}")
    
    return clima


def mostrar_estacion(nombre):
    """
    Muestra el clima de una estación específica.
    
    Args:
        nombre: Nombre de la estación a buscar
    """
    print(f"\n🔍 Buscando estación: {nombre}")
    print("-" * 40)
    
    clima = obtener_clima()
    
    if not clima['exito']:
        print(f"\n❌ Error: {clima['error']}")
        return
    
    estacion = buscar_estacion(nombre, clima['estaciones'])
    
    if estacion:
        print(f"\n📍 {estacion['nombre']}")
        print(f"   🌡️  Temperatura: {estacion['temperatura']}°C")
        print(f"   🌧️  Precipitación: {estacion['precipitacion']} mm")
        print(f"   📍 Ubicación: {estacion['latitud']}, {estacion['longitud']}")
    else:
        print(f"\n⚠️  No se encontró la estación '{nombre}'")
        print("\nEstaciones disponibles con datos:")
        
        estaciones_validas = [e for e in clima['estaciones'] if e.get('temperatura') is not None]
        for est in estaciones_validas[:15]:
            print(f"   - {est['nombre']}")
        
        if len(estaciones_validas) > 15:
            print(f"   ... y {len(estaciones_validas) - 15} más")


def listar_estaciones():
    """
    Lista todas las estaciones meteorológicas disponibles.
    """
    print("\n📋 Listando estaciones meteorológicas...")
    print("-" * 40)
    
    clima = obtener_clima()
    
    if not clima['exito']:
        print(f"\n❌ Error: {clima['error']}")
        return
    
    estaciones = clima['estaciones']
    estaciones_con_temp = [e for e in estaciones if e.get('temperatura') is not None]
    estaciones_sin_temp = [e for e in estaciones if e.get('temperatura') is None]
    
    print(f"\n🌡️  Estaciones con datos ({len(estaciones_con_temp)}):")
    print("-" * 40)
    
    # Ordenar por temperatura descendente
    estaciones_con_temp.sort(key=lambda x: x['temperatura'], reverse=True)
    
    for est in estaciones_con_temp:
        temp = est['temperatura']
        emoji = "🔥" if temp > 30 else "❄️" if temp < 10 else "🌡️"
        print(f"   {emoji} {est['nombre']}: {temp}°C")
    
    if estaciones_sin_temp:
        print(f"\n⚠️  Estaciones sin datos actuales ({len(estaciones_sin_temp)}):")
        for est in estaciones_sin_temp[:5]:
            print(f"   - {est['nombre']}")
        if len(estaciones_sin_temp) > 5:
            print(f"   ... y {len(estaciones_sin_temp) - 5} más")
    
    print(f"\n📊 Total: {len(estaciones)} estaciones")


def mostrar_resumen():
    """
    Muestra un resumen corto del clima.
    """
    clima = obtener_clima()
    
    if clima['exito']:
        resumen = generar_resumen(clima)
        print(resumen)
    else:
        print(f"❌ Error: {clima['error']}")


def main():
    """
    Función principal con manejo de argumentos de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description='🌤️  Clima San Luis - Obtiene el clima de San Luis, Argentina',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  python main.py                        Obtiene el clima completo
  python main.py --daemon               Ejecuta en modo continuo
  python main.py --hora 08:00 --daemon  Programa ejecución a las 8:00
  python main.py --estacion "Merlo"     Clima de una estación específica
  python main.py --listar               Lista todas las estaciones
  python main.py --resumen              Muestra resumen corto

Fuente: https://clima.sanluis.gob.ar/ (REM - Gobierno de San Luis)
        '''
    )
    
    parser.add_argument(
        '--daemon', '-d',
        action='store_true',
        help='Ejecutar en modo daemon (continuo)'
    )
    
    parser.add_argument(
        '--hora', '-t',
        type=str,
        default=HORA_EJECUCION,
        help=f'Hora de ejecución diaria en modo daemon (default: {HORA_EJECUCION})'
    )
    
    parser.add_argument(
        '--estacion', '-e',
        type=str,
        help='Mostrar clima de una estación específica'
    )
    
    parser.add_argument(
        '--listar', '-l',
        action='store_true',
        help='Listar todas las estaciones disponibles'
    )
    
    parser.add_argument(
        '--resumen', '-r',
        action='store_true',
        help='Mostrar resumen corto del clima'
    )
    
    parser.add_argument(
        '--archivo', '-a',
        type=str,
        help='Guardar reporte en archivo específico'
    )
    
    parser.add_argument(
        '--silencioso', '-s',
        action='store_true',
        help='Modo silencioso (sin salida en consola)'
    )
    
    args = parser.parse_args()
    
    # Banner
    if not args.silencioso:
        print("\n" + "=" * 50)
        print("🌤️  CLIMA SAN LUIS")
        print(f"📅 {formato_fecha_espanol()}")
        print("=" * 50)
    
    try:
        if args.daemon:
            # Modo daemon
            programar_tarea_diaria(args.hora)
            ejecutar_daemon()
        
        elif args.estacion:
            # Mostrar estación específica
            mostrar_estacion(args.estacion)
        
        elif args.listar:
            # Listar estaciones
            listar_estaciones()
        
        elif args.resumen:
            # Mostrar resumen
            mostrar_resumen()
        
        else:
            # Ejecución normal
            clima = ejecutar_clima()
            
            # Guardar en archivo específico si se solicita
            if args.archivo and clima['exito']:
                notificar_archivo(clima, args.archivo)
                print(f"\n📄 Reporte guardado en: {args.archivo}")
    
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()










