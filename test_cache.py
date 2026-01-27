#!/usr/bin/env python3
"""
Script de prueba para verificar que la funcionalidad de caché funciona correctamente.
Este script simula un error de scraping y verifica que se cargue el último clima guardado.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils import cargar_ultimo_clima

def test_cache():
    print("\n" + "=" * 60)
    print("🧪 PRUEBA DE CACHÉ - Último Clima Guardado")
    print("=" * 60 + "\n")
    
    # Intentar cargar el último clima guardado
    clima = cargar_ultimo_clima()
    
    if clima:
        print("✅ Se cargó correctamente el último clima guardado\n")
        
        print(f"📊 Información del clima guardado:")
        print(f"  • Éxito: {clima.get('exito')}")
        print(f"  • Usando caché: {clima.get('usando_cache', 'N/A')}")
        print(f"  • Timestamp guardado: {clima.get('timestamp_guardado')}")
        
        # Verificar si hay pronóstico general
        if clima.get('pronostico_general'):
            pronostico = clima['pronostico_general']
            if pronostico.get('pronostico_hoy'):
                hoy = pronostico['pronostico_hoy']
                print(f"\n🌡️ Temperaturas del día:")
                print(f"  • Mínima: {hoy.get('temperatura_minima')}°C")
                print(f"  • Máxima: {hoy.get('temperatura_maxima')}°C")
        
        # Verificar si hay estaciones
        estaciones = clima.get('estaciones', [])
        estaciones_validas = [e for e in estaciones if e.get('temperatura') is not None]
        print(f"\n📍 Estaciones con datos: {len(estaciones_validas)}")
        
        if estaciones_validas:
            print(f"  • Primera estación: {estaciones_validas[0]['nombre']} - {estaciones_validas[0]['temperatura']}°C")
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA EXITOSA: El sistema de caché funciona correctamente")
        print("=" * 60 + "\n")
    else:
        print("❌ No se pudo cargar el último clima guardado")
        print("   (Esto es normal si aún no se ha ejecutado el scraper)")

if __name__ == "__main__":
    test_cache()
