import schedule
import time
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import HORA_EJECUCION
from src.scraper import obtener_clima
from src.notifier import notificar_consola, notificar_archivo, notificar_escritorio
from src.utils import setup_logger

logger = setup_logger()


def tarea_clima():
    """
    Tarea principal que obtiene el clima y envía notificaciones.
    """
    logger.info("=" * 50)
    logger.info("Iniciando tarea de obtención del clima")
    logger.info("=" * 50)
    
    try:
        # Obtener datos del clima
        clima = obtener_clima()
        
        if clima['exito']:
            logger.info("Datos del clima obtenidos correctamente")
            
            # Notificar en consola
            notificar_consola(clima)
            
            # Guardar en archivo
            ruta_archivo = notificar_archivo(clima)
            logger.info(f"Reporte guardado en: {ruta_archivo}")
            
            # Intentar notificación de escritorio
            notificar_escritorio(clima)
            
        else:
            logger.error(f"Error al obtener el clima: {clima['error']}")
            print(f"\n❌ Error: {clima['error']}")
        
        logger.info("Tarea completada")
        
    except Exception as e:
        logger.error(f"Error inesperado en tarea_clima: {e}")
        print(f"\n❌ Error inesperado: {e}")


def programar_tarea_diaria(hora=None):
    """
    Programa la ejecución diaria del clima.
    
    Args:
        hora: Hora de ejecución en formato "HH:MM" (usa config por defecto)
    """
    if hora is None:
        hora = HORA_EJECUCION
    
    logger.info(f"Programando tarea diaria para las {hora}")
    
    # Programar la tarea
    schedule.every().day.at(hora).do(tarea_clima)
    
    print(f"\n✅ Tarea programada para ejecutarse todos los días a las {hora}")
    print("   Presiona Ctrl+C para detener\n")


def ejecutar_daemon():
    """
    Ejecuta el scheduler en modo daemon (continuo).
    Mantiene el programa corriendo y ejecuta las tareas programadas.
    """
    logger.info("Iniciando modo daemon")
    
    programar_tarea_diaria()
    
    # Mostrar próxima ejecución
    proxima = schedule.next_run()
    if proxima:
        print(f"📅 Próxima ejecución: {proxima.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
            
    except KeyboardInterrupt:
        logger.info("Scheduler detenido por el usuario")
        print("\n\n👋 Scheduler detenido. ¡Hasta luego!")


def ejecutar_ahora():
    """
    Ejecuta la tarea de clima inmediatamente (una sola vez).
    """
    logger.info("Ejecutando tarea inmediatamente")
    tarea_clima()


def mostrar_estado():
    """
    Muestra el estado actual del scheduler.
    """
    print("\n📊 Estado del Scheduler")
    print("-" * 40)
    print(f"   Hora configurada: {HORA_EJECUCION}")
    print(f"   Hora actual: {datetime.now().strftime('%H:%M:%S')}")
    
    trabajos = schedule.get_jobs()
    if trabajos:
        print(f"   Tareas programadas: {len(trabajos)}")
        proxima = schedule.next_run()
        if proxima:
            print(f"   Próxima ejecución: {proxima.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("   No hay tareas programadas")
    
    print("-" * 40)


def main():
    """
    Función principal con manejo de argumentos.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Scheduler para obtener el clima de San Luis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos de uso:
  python scheduler.py              # Ejecuta una vez ahora
  python scheduler.py --daemon     # Ejecuta en modo continuo
  python scheduler.py --hora 08:00 # Programa para las 8:00
  python scheduler.py --estado     # Muestra estado del scheduler
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
        default=None,
        help=f'Hora de ejecución diaria (formato HH:MM, default: {HORA_EJECUCION})'
    )
    
    parser.add_argument(
        '--estado', '-s',
        action='store_true',
        help='Mostrar estado del scheduler'
    )
    
    parser.add_argument(
        '--una-vez', '-1',
        action='store_true',
        help='Ejecutar una sola vez ahora (default)'
    )
    
    args = parser.parse_args()
    
    print("\n🌤️  Clima San Luis - Scheduler")
    print("=" * 40)
    
    if args.estado:
        mostrar_estado()
    elif args.daemon:
        if args.hora:
            programar_tarea_diaria(args.hora)
        ejecutar_daemon()
    else:
        # Por defecto, ejecutar una vez
        ejecutar_ahora()


if __name__ == "__main__":
    main()









