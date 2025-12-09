# Alternativas de Deploy para Clima San Luis

Guía con múltiples opciones de deploy para el proyecto.

## 🚀 Opción 1: Render (Más Simple)

Render es una excelente alternativa a Railway, y ya tenemos la configuración lista.

### Pasos:

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente `render.yaml`
5. Configura variables de entorno:
   - `FLASK_ENV` = `production`
   - `FRONTEND_URL` = `https://tu-app.onrender.com`
   - `VITE_API_URL` = `https://tu-app.onrender.com/api`

### Ventajas:
- ✅ Ya tenemos `render.yaml` configurado
- ✅ Muy fácil de configurar
- ✅ Plan gratuito disponible

---

## 🚂 Opción 2: Railway con Dockerfile Simplificado

Si quieres seguir intentando con Railway, usa el Dockerfile simplificado.

### Pasos:

1. Renombra `Dockerfile` a `Dockerfile.railway.backup`
2. Renombra `Dockerfile.simple` a `Dockerfile`
3. Haz push y redeploy

```bash
mv Dockerfile Dockerfile.railway.backup
mv Dockerfile.simple Dockerfile
git add Dockerfile
git commit -m "Use simplified Dockerfile"
git push
```

---

## ✈️ Opción 3: Fly.io

Fly.io es otra excelente opción con buen plan gratuito.

### Instalación:

```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Desplegar
fly launch
```

### Configuración:

1. Usa `Dockerfile.fly` (renómbralo a `Dockerfile`)
2. O configura con `fly.toml` que ya está creado

### Ventajas:
- ✅ Muy rápido
- ✅ Plan gratuito generoso
- ✅ Deploy global

---

## 🟣 Opción 4: Heroku

Heroku sigue siendo una opción popular.

### Pasos:

1. Instala Heroku CLI:
```bash
# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Login:
```bash
heroku login
```

3. Crea la app:
```bash
heroku create clima-san-luis
```

4. Configura buildpacks:
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs --index 1
```

5. Variables de entorno:
```bash
heroku config:set FLASK_ENV=production
heroku config:set FRONTEND_URL=https://clima-san-luis.herokuapp.com
heroku config:set VITE_API_URL=https://clima-san-luis.herokuapp.com/api
```

6. Deploy:
```bash
git push heroku main
```

### Ventajas:
- ✅ Muy establecido
- ✅ Bueno para proyectos pequeños

### Desventajas:
- ❌ Plan gratuito limitado
- ❌ Puede ser más lento

---

## 🌊 Opción 5: DigitalOcean App Platform

Otra opción sólida y confiable.

### Pasos:

1. Ve a [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click en "Create App"
3. Conecta tu repositorio
4. Configura:
   - **Build Command**: `pip install -r backend/requirements.txt && cd frontend && npm install && npm run build`
   - **Run Command**: `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2`
   - **Environment**: Python
5. Agrega variables de entorno
6. Deploy

### Ventajas:
- ✅ Muy confiable
- ✅ Buen soporte

---

## 🐳 Opción 6: Docker + Servidor VPS (Más Control)

Si tienes acceso a un VPS, puedes usar Docker directamente.

### Pasos:

1. En tu VPS, instala Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

2. Clona el repositorio:
```bash
git clone tu-repo
cd Clima-San-Luis
```

3. Construye y ejecuta:
```bash
docker build -t clima-san-luis .
docker run -d -p 80:5000 \
  -e FLASK_ENV=production \
  -e FRONTEND_URL=http://tu-dominio.com \
  -e VITE_API_URL=http://tu-dominio.com/api \
  --name clima-san-luis \
  clima-san-luis
```

### Ventajas:
- ✅ Control total
- ✅ Sin límites de plataforma
- ✅ Más económico a largo plazo

---

## 🔄 Opción 7: Deploy Separado (Frontend + Backend)

Separar el frontend y backend puede ser más fácil.

### Frontend (Vercel/Netlify):

1. Ve a [Vercel](https://vercel.com/) o [Netlify](https://netlify.com/)
2. Conecta el repositorio
3. Configura:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Environment Variable**: `VITE_API_URL=https://tu-backend.railway.app/api`

### Backend (Railway/Render):

1. Despliega solo el backend usando uno de los métodos anteriores
2. Configura CORS para permitir el dominio del frontend

---

## 📊 Comparación Rápida

| Plataforma | Dificultad | Plan Gratuito | Velocidad | Recomendación |
|------------|-----------|---------------|-----------|---------------|
| **Render** | ⭐ Fácil | ✅ Sí | ⚡ Rápido | ⭐⭐⭐⭐⭐ |
| **Fly.io** | ⭐⭐ Media | ✅ Sí | ⚡⚡ Muy Rápido | ⭐⭐⭐⭐ |
| **Railway** | ⭐⭐ Media | ✅ Sí | ⚡ Rápido | ⭐⭐⭐ |
| **Heroku** | ⭐⭐ Media | ⚠️ Limitado | ⚡ Normal | ⭐⭐⭐ |
| **DigitalOcean** | ⭐⭐ Media | ⚠️ Trial | ⚡ Normal | ⭐⭐⭐⭐ |
| **VPS + Docker** | ⭐⭐⭐ Difícil | 💰 Pago | ⚡ Variable | ⭐⭐⭐⭐ |

---

## 🎯 Recomendación

**Para empezar rápido**: Usa **Render** - ya tenemos todo configurado.

**Para máxima confiabilidad**: Usa **Fly.io** - muy rápido y confiable.

**Para control total**: Usa **VPS + Docker** - más trabajo pero más control.

---

## 📝 Archivos de Configuración Disponibles

- `render.yaml` - Para Render ✅
- `Dockerfile` - Para Railway/Docker ✅

---

## 🔧 Próximos Pasos

1. **Elige una plataforma** de las opciones arriba
2. **Sigue los pasos** específicos para esa plataforma
3. **Configura variables de entorno** necesarias
4. **Haz deploy** y verifica que funcione

¿Necesitas ayuda con alguna plataforma específica?

