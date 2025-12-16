#!/bin/bash
# Script de build para preparar el proyecto para deploy
# Este script construye el frontend y lo prepara para ser servido por el backend

set -e  # Salir si hay algún error

echo "🚀 Iniciando build para producción..."
echo "=================================="

# Verificar que estamos en el directorio raíz del proyecto
if [ ! -f "backend/app.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Este script debe ejecutarse desde el directorio raíz del proyecto"
    exit 1
fi

# Paso 1: Instalar dependencias del backend (si es necesario)
echo ""
echo "📦 Instalando dependencias del backend..."
cd backend
if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
fi
cd ..

# Paso 2: Instalar dependencias del frontend
echo ""
echo "📦 Instalando dependencias del frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

# Paso 3: Construir el frontend
echo ""
echo "🔨 Construyendo frontend para producción..."
npm run build

# Verificar que el build fue exitoso
if [ ! -d "dist" ]; then
    echo "❌ Error: El build del frontend falló. No se encontró el directorio dist/"
    exit 1
fi

echo "✅ Frontend construido exitosamente en frontend/dist/"

# Paso 4: Los archivos estáticos ya están en frontend/dist/
# El backend los servirá desde esa ubicación configurada en app.py
echo ""
echo "✅ Build completado!"
echo ""
echo "📝 Nota: Los archivos estáticos están en frontend/dist/"
echo "   El backend está configurado para servirlos desde allí."
echo ""
echo "🚀 Para ejecutar en producción:"
echo "   cd backend && gunicorn wsgi:app"

cd ..



