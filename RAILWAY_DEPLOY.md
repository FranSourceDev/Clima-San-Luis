# Guía de Deploy en Railway - Clima San Luis

Guía paso a paso para desplegar el proyecto en Railway.

## 📋 Prerequisitos

- Cuenta en [Railway](https://railway.app/) (puedes usar GitHub para registrarte)
- Repositorio Git del proyecto subido a GitHub, GitLab o Bitbucket
- Tu repositorio debe tener el código listo para deploy

## 🚀 Pasos para Deploy

### Paso 1: Conectar el Repositorio

1. Ve a [Railway Dashboard](https://railway.app/dashboard)
2. Haz click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"** (o GitLab/Bitbucket si prefieres)
4. Autoriza Railway para acceder a tus repositorios
5. Selecciona el repositorio `Clima-San-Luis` (o el nombre que tenga tu repo)

### Paso 2: Configurar el Servicio

Railway debería detectar automáticamente:
- El `Procfile` para el comando de inicio
- El `railway.json` para la configuración de build

**Verifica la configuración:**
1. En la configuración del servicio, asegúrate de que:
   - **Build Command**: `pip install -r backend/requirements.txt && cd frontend && npm install && npm run build`
   - **Start Command**: `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`

**Nota**: Si Railway no detecta el `Procfile`, puedes configurarlo manualmente en Settings → Deploy.

### Paso 3: Configurar Variables de Entorno

1. Ve a la pestaña **"Variables"** en el servicio
2. Agrega las siguientes variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Ambiente de Flask |
| `FRONTEND_URL` | `https://tu-app.up.railway.app` | URL del frontend (se actualizará después) |
| `VITE_API_URL` | `https://tu-app.up.railway.app/api` | URL de la API (se actualizará después) |

**Importante**: 
- La variable `PORT` se asigna automáticamente por Railway, NO la agregues manualmente.
- Al principio, usa una URL temporal. Después del primer deploy, Railway te dará la URL real.

### Paso 4: Primer Deploy

1. Railway comenzará automáticamente el build al conectar el repositorio
2. Puedes ver el progreso en la pestaña **"Deployments"**
3. El build puede tardar varios minutos la primera vez

### Paso 5: Obtener la URL y Actualizar Variables

1. Una vez que el deploy esté completo, Railway te dará una URL como:
   - `https://clima-san-luis-production.up.railway.app`

2. **Actualiza las variables de entorno** con la URL real:
   - `FRONTEND_URL` = `https://clima-san-luis-production.up.railway.app`
   - `VITE_API_URL` = `https://clima-san-luis-production.up.railway.app/api`

3. **Haz un nuevo deploy** para que el frontend se reconstruya con la URL correcta:
   - Ve a la pestaña **"Deployments"**
   - Click en **"Redeploy"** del último deployment

### Paso 6: Configurar Dominio Personalizado (Opcional)

1. Ve a **Settings** → **Networking**
2. Click en **"Generate Domain"** para obtener un dominio aleatorio
3. O agrega tu propio dominio personalizado

## ✅ Verificación

Después del deploy, verifica que todo funcione:

1. **Health Check**: 
   - Visita: `https://tu-app.up.railway.app/health`
   - Debe retornar: `{"status":"ok"}`

2. **API Info**:
   - Visita: `https://tu-app.up.railway.app/api/info`
   - Debe mostrar información de la API

3. **Frontend**:
   - Visita: `https://tu-app.up.railway.app/`
   - Debe mostrar el dashboard de Clima San Luis

4. **API Endpoints**:
   - Verifica que las peticiones funcionen:
     - `/api/clima`
     - `/api/estaciones`
     - `/api/pronostico`

## 🔧 Troubleshooting

### Problema: Build falla

**Error común**: "Node.js not found"
- **Solución**: Railway usa Nixpacks que detecta automáticamente Node.js. Si falla, verifica que el `package.json` esté en `frontend/`.

**Error común**: "Module not found"
- **Solución**: Verifica que todas las dependencias estén en `backend/requirements.txt` y `frontend/package.json`.

### Problema: Frontend no carga (error 503)

- Verifica que el build del frontend se completó correctamente
- Revisa los logs del deploy para ver errores
- Asegúrate de que `frontend/dist/` se creó durante el build

### Problema: CORS errors

- Verifica que `FRONTEND_URL` tenga el valor correcto (sin barra final)
- Verifica que la URL coincida exactamente con la URL de Railway
- Haz un redeploy después de cambiar variables de entorno

### Problema: API no responde

- Verifica los logs del servicio en Railway
- Asegúrate de que gunicorn esté corriendo
- Verifica que el puerto sea `$PORT` (no un número fijo)

### Ver Logs

1. Ve a la pestaña **"Deployments"**
2. Click en el deployment que quieres revisar
3. Ve a la sección **"Logs"** para ver los logs del build y del runtime

## 📊 Monitoreo

Railway ofrece:
- **Logs en tiempo real**: Ve la pestaña "Logs" del servicio
- **Métricas**: CPU, memoria, etc. en el dashboard
- **Deployments**: Historial de todos los deploys

## 🔄 Deploys Automáticos

Por defecto, Railway hace deploy automático cuando:
- Haces push a la rama principal (main/master)
- Cambias variables de entorno
- Haces redeploy manual

Para desactivar deploys automáticos:
- Settings → Source → Desactivar "Auto Deploy"

## 💰 Costos

- Railway ofrece un plan gratuito con:
  - $5 de crédito gratis por mes
  - Suficiente para una aplicación pequeña como esta
- Si superas el límite, se pausa automáticamente

## 📚 Recursos

- [Railway Docs](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Nixpacks Docs](https://nixpacks.com/docs)

