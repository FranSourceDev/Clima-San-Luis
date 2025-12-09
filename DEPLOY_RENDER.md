# Guía de Deploy en Render - Clima San Luis

Guía paso a paso para desplegar el proyecto en Render.

## 📋 Prerequisitos

- Cuenta en [Render](https://render.com/) (puedes usar GitHub para registrarte)
- Repositorio Git del proyecto en GitHub, GitLab o Bitbucket
- El archivo `render.yaml` debe estar en la raíz del repositorio

## 🚀 Pasos para Deploy

### Paso 1: Crear Cuenta y Conectar Repositorio

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Si no tienes cuenta, haz click en **"Get Started for Free"**
3. Autoriza Render para acceder a tu repositorio de GitHub/GitLab/Bitbucket
4. Una vez en el dashboard, haz click en **"New +"** en la parte superior
5. Selecciona **"Blueprint"** (Render detectará automáticamente el `render.yaml`)

**O** si prefieres crear manualmente:

1. Haz click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio
3. Render detectará automáticamente el `render.yaml`

### Paso 2: Configurar el Servicio

Si usas Blueprint (recomendado):
- Render leerá automáticamente `render.yaml`
- Solo necesitas darle un nombre al servicio

Si creas manualmente:
- **Name**: `clima-san-luis` (o el nombre que prefieras)
- **Environment**: `Python 3`
- **Build Command**: (Render lo detectará de `render.yaml`)
- **Start Command**: (Render lo detectará de `render.yaml`)

### Paso 3: Configurar Variables de Entorno

**IMPORTANTE**: Necesitas configurar estas variables después del primer deploy.

1. Ve a la pestaña **"Environment"** en tu servicio
2. Agrega las siguientes variables:

| Variable | Valor Inicial | Valor Final (después del deploy) |
|----------|---------------|----------------------------------|
| `FLASK_ENV` | `production` | `production` |
| `FRONTEND_URL` | `https://clima-san-luis.onrender.com` | Tu URL real de Render |
| `VITE_API_URL` | `https://clima-san-luis.onrender.com/api` | Tu URL real + `/api` |

**Nota**: 
- La variable `PORT` se asigna automáticamente por Render, NO la agregues
- Usa URLs temporales al principio, luego actualiza con la URL real que Render te dé

### Paso 4: Primer Deploy

1. Click en **"Create Web Service"** (o **"Apply"** si usas Blueprint)
2. Render comenzará automáticamente el build
3. Puedes ver el progreso en tiempo real en los logs

**El build puede tardar 5-10 minutos la primera vez**

### Paso 5: Obtener URL y Actualizar Variables

1. Una vez que el deploy esté completo, Render te dará una URL como:
   - `https://clima-san-luis-xxxx.onrender.com`

2. **Actualiza las variables de entorno** con la URL real:
   - Ve a **Environment** en tu servicio
   - Actualiza `FRONTEND_URL` con tu URL real (sin barra final)
   - Actualiza `VITE_API_URL` con tu URL real + `/api`

3. **Haz un redeploy** para que el frontend se reconstruya con la URL correcta:
   - Ve a la pestaña **"Manual Deploy"**
   - Click en **"Clear build cache & deploy"**

### Paso 6: Configurar Auto-Deploy (Opcional)

Por defecto, Render hace deploy automático cuando:
- Haces push a la rama principal (main/master)
- Cambias variables de entorno

Para configurar manualmente:
- Ve a **Settings** → **Auto-Deploy**
- Elige la rama que quieres usar para deploys automáticos

## ✅ Verificación

Después del deploy, verifica que todo funcione:

1. **Health Check**: 
   - Visita: `https://tu-app.onrender.com/health`
   - Debe retornar: `{"status":"ok"}`

2. **API Info**:
   - Visita: `https://tu-app.onrender.com/api/info`
   - Debe mostrar información de la API

3. **Frontend**:
   - Visita: `https://tu-app.onrender.com/`
   - Debe mostrar el dashboard de Clima San Luis

4. **API Endpoints**:
   - Verifica que funcionen:
     - `/api/clima`
     - `/api/estaciones`
     - `/api/pronostico`

## 🔧 Troubleshooting

### Problema: Build falla - "Node.js not found"

**Solución**: 
- Verifica que `render.yaml` tiene el buildCommand correcto
- Render debería detectar automáticamente Node.js desde el `package.json`

### Problema: Build falla - "Module not found"

**Solución**:
- Verifica que todas las dependencias estén en `backend/requirements.txt` y `frontend/package.json`
- Revisa los logs del build para ver qué módulo falta

### Problema: Frontend no carga (error 503)

**Solución**:
- Verifica que el build del frontend se completó (`npm run build`)
- Revisa los logs para ver si `frontend/dist/` se creó
- Asegúrate de que Flask está configurado para servir archivos estáticos

### Problema: CORS errors

**Solución**:
- Verifica que `FRONTEND_URL` tenga el valor correcto
- Asegúrate de que la URL coincida exactamente (sin barra final)
- Haz un redeploy después de cambiar variables de entorno

### Problema: App se "duerme" después de inactividad

**Solución**:
- El plan gratuito de Render "duerme" las apps después de 15 minutos de inactividad
- La primera solicitud después de dormir puede tardar ~30 segundos en "despertar"
- Para evitar esto, considera el plan Starter ($7/mes)

## 📊 Monitoreo

Render ofrece:
- **Logs en tiempo real**: Ve la pestaña "Logs" del servicio
- **Métricas**: CPU, memoria, etc. en el dashboard
- **Deployments**: Historial de todos los deploys

## 💰 Planes y Límites

- **Plan Gratuito**:
  - Apps se "duermen" después de 15 min de inactividad
  - 750 horas gratis por mes
  - Suficiente para desarrollo y proyectos pequeños

- **Plan Starter** ($7/mes):
  - Apps siempre despiertas
  - Mejor rendimiento
  - Recomendado para producción

## 📝 Archivos Importantes

- `render.yaml` - Configuración de Render (ya está configurado)
- `backend/wsgi.py` - Servidor WSGI
- `backend/requirements.txt` - Dependencias Python
- `frontend/package.json` - Dependencias Node.js

## 🔄 Actualización y Redeploy

Para actualizar la aplicación:

1. Haz cambios en tu código
2. Haz commit y push:
   ```bash
   git add .
   git commit -m "Actualización"
   git push
   ```
3. Render hará deploy automático (si está configurado)

Para redeploy manual:
- Ve a **Manual Deploy** en tu servicio
- Click en **"Deploy latest commit"**

## 📚 Recursos

- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com/)
- [Render Status](https://status.render.com/)

## ✨ ¡Listo!

Tu aplicación debería estar funcionando en Render. Si tienes algún problema, revisa los logs en la pestaña "Logs" del servicio.

