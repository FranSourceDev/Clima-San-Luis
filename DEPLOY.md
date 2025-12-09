# Guía de Deploy - Clima San Luis

Esta guía explica cómo desplegar el proyecto Clima San Luis en diferentes plataformas cloud.

## 📋 Requisitos Previos

- Cuenta en la plataforma cloud elegida (Railway, Render, etc.)
- Repositorio Git del proyecto
- Node.js 18+ (para build del frontend)
- Python 3.12+ (para el backend)

## 🏗️ Arquitectura del Deploy

El proyecto está configurado para deploy monolítico:
- **Backend Flask**: Sirve la API REST en `/api/*`
- **Frontend React**: Archivos estáticos construidos y servidos por Flask
- **Servidor WSGI**: Gunicorn para producción

## 🔧 Variables de Entorno

Antes de hacer deploy, asegúrate de configurar estas variables de entorno:

### Variables Requeridas

- `FLASK_ENV`: `production`
- `PORT`: Puerto asignado automáticamente por la plataforma (no configurar manualmente)
- `FRONTEND_URL`: URL completa del frontend en producción (para CORS)
- `VITE_API_URL`: URL completa del backend API (se usa durante el build del frontend)

### Ejemplo de Variables

```
FLASK_ENV=production
FRONTEND_URL=https://tu-app.onrender.com
VITE_API_URL=https://tu-app.onrender.com/api
```

## 🚀 Deploy en Render

### Paso 1: Crear nuevo Web Service

1. Ir a [Render Dashboard](https://dashboard.render.com/)
2. Click en "New +" → "Web Service"
3. Conectar tu repositorio de GitHub

### Paso 2: Configurar el servicio

- **Name**: `clima-san-luis` (o el nombre que prefieras)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r backend/requirements.txt && cd frontend && npm install && npm run build
  ```
- **Start Command**:
  ```bash
  cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
  ```

### Paso 3: Configurar Variables de Entorno

En la sección "Environment Variables", agregar:

- `FLASK_ENV` = `production`
- `FRONTEND_URL` = `https://tu-app.onrender.com` (reemplazar con tu URL)
- `VITE_API_URL` = `https://tu-app.onrender.com/api` (reemplazar con tu URL)

**Nota**: La variable `PORT` se asigna automáticamente por Render.

### Paso 4: Deploy

Click en "Create Web Service". Render construirá y desplegará automáticamente.

**Alternativa**: Si prefieres usar el archivo `render.yaml`, Render lo detectará automáticamente.

## 🚂 Deploy en Railway

### Paso 1: Crear nuevo proyecto

1. Ir a [Railway Dashboard](https://railway.app/)
2. Click en "New Project"
3. Conectar tu repositorio de GitHub

### Paso 2: Configurar el servicio

Railway detectará automáticamente el `Procfile` y lo usará.

Si necesitas configuración manual:
- **Build Command**: 
  ```bash
  pip install -r backend/requirements.txt && cd frontend && npm install && npm run build
  ```
- **Start Command**: Ya está configurado en el `Procfile`

### Paso 3: Configurar Variables de Entorno

En la sección "Variables", agregar:

- `FLASK_ENV` = `production`
- `FRONTEND_URL` = `https://tu-app.up.railway.app` (reemplazar con tu URL)
- `VITE_API_URL` = `https://tu-app.up.railway.app/api` (reemplazar con tu URL)

**Nota**: `PORT` se asigna automáticamente por Railway.

### Paso 4: Deploy

Railway hará deploy automáticamente al hacer push a la rama main.

## 🐳 Deploy con Docker (Opcional)

Para usar Docker, necesitarías crear un `Dockerfile`. Esto no está incluido en el plan actual, pero puede agregarse si se necesita.

## 📝 Build Local para Pruebas

Antes de hacer deploy, puedes probar el build localmente:

```bash
# Ejecutar el script de build
./build.sh

# Probar el servidor de producción
cd backend
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2
```

Luego acceder a `http://localhost:5000` para verificar que todo funciona.

## ✅ Verificación Post-Deploy

Después del deploy, verifica:

1. **Health Check**: `https://tu-app.onrender.com/health` debe retornar `{"status":"ok"}`
2. **API**: `https://tu-app.onrender.com/api/` debe mostrar información de la API
3. **Frontend**: `https://tu-app.onrender.com/` debe mostrar el dashboard
4. **CORS**: Verificar que las peticiones desde el frontend funcionan correctamente

## 🔍 Troubleshooting

### Problema: Frontend no carga
- Verificar que el build se ejecutó correctamente
- Verificar que `frontend/dist/` existe después del build
- Verificar que Flask está configurado para servir archivos estáticos desde `../frontend/dist`

### Problema: CORS errors
- Verificar que `FRONTEND_URL` está configurada correctamente
- Verificar que la URL en `FRONTEND_URL` coincide exactamente con la URL de producción

### Problema: API no responde
- Verificar que `PORT` se asigna automáticamente
- Verificar logs del servicio para errores
- Verificar que todas las dependencias están en `backend/requirements.txt`

### Problema: Build falla
- Verificar que Node.js está disponible durante el build
- Verificar que todas las dependencias están correctamente especificadas
- Revisar logs del build para errores específicos

## 📚 Recursos Adicionales

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [Gunicorn Docs](https://gunicorn.org/)
- [Vite Build Docs](https://vitejs.dev/guide/build.html)

