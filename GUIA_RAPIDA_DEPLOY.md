# Guía Rápida de Deploy - Clima San Luis

## 🎯 Recomendación Principal: **Render**

Render es la opción más fácil y ya está completamente configurada.

### Pasos Rápidos para Render:

1. **Ve a**: https://dashboard.render.com/
2. **Click en**: "New +" → "Web Service"
3. **Conecta**: Tu repositorio de GitHub
4. **Render detectará automáticamente**: `render.yaml`
5. **Configura variables** (después del primer deploy):
   - `FLASK_ENV` = `production`
   - `FRONTEND_URL` = `https://tu-app.onrender.com` (tu URL real)
   - `VITE_API_URL` = `https://tu-app.onrender.com/api` (tu URL real + /api)

**¡Eso es todo!** Render hará el resto automáticamente.

---

## ⚡ Opciones Rápidas por Prioridad

### 1. **Render** ⭐⭐⭐⭐⭐ (RECOMENDADO)
- ✅ Más fácil
- ✅ Ya configurado (`render.yaml`)
- ✅ Plan gratuito
- ⏱️ 5 minutos para deploy

### 2. **Fly.io** ⭐⭐⭐⭐
- ✅ Muy rápido
- ✅ Plan gratuito generoso
- ⏱️ 10 minutos para deploy

```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Login y deploy
fly auth login
fly launch
# Selecciona Dockerfile.fly cuando pregunte
```

### 3. **VPS + Docker** ⭐⭐⭐⭐
- ✅ Control total
- ✅ Sin límites
- ⏱️ 15-20 minutos para configurar

```bash
# En tu VPS
git clone tu-repo
cd Clima-San-Luis
docker build -t clima-san-luis .
docker run -d -p 80:5000 -e FLASK_ENV=production clima-san-luis
```

---

## 🔄 Cambiar entre Configuraciones

### Para Render:
```bash
# Ya está listo, solo usa render.yaml
```

### Para Railway:
```bash
# Opción 1: Dockerfile original
cp Dockerfile Dockerfile.railway

# Opción 2: Dockerfile simplificado
cp Dockerfile.simple Dockerfile

# Opción 3: Dockerfile alternativo
cp Dockerfile.alternative Dockerfile
```

### Para Fly.io:
```bash
cp Dockerfile.fly Dockerfile
# fly.toml ya está configurado
```

---

## 🆘 Si Todo Falla: Deploy Separado

### Frontend en Vercel (Gratis):
1. Ve a vercel.com
2. Conecta repositorio
3. Configura:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment: `VITE_API_URL=https://tu-backend.com/api`

### Backend en Render/Railway:
1. Despliega solo el backend
2. Configura CORS para permitir el dominio de Vercel

---

## 📋 Checklist Pre-Deploy

- [ ] Variables de entorno configuradas
- [ ] `FRONTEND_URL` apunta a la URL correcta
- [ ] `VITE_API_URL` apunta a la API correcta
- [ ] Build del frontend funciona localmente
- [ ] Backend funciona localmente con `gunicorn`

---

## 🔍 Verificación Post-Deploy

Después del deploy, verifica:

1. **Health Check**: `https://tu-app.com/health` → `{"status":"ok"}`
2. **API Info**: `https://tu-app.com/api/info` → Información de la API
3. **Frontend**: `https://tu-app.com/` → Dashboard carga
4. **CORS**: Sin errores en la consola del navegador

---

## 💡 Tips

- **Render**: La mejor opción si quieres algo que "simplemente funcione"
- **Fly.io**: Excelente si necesitas velocidad y confiabilidad
- **VPS**: Mejor si ya tienes un servidor o quieres control total
- **Separado**: Útil si tienes problemas con el deploy monolítico

---

## 📞 Próximos Pasos

1. **Elige Render** si quieres la solución más rápida
2. **O Fly.io** si quieres algo diferente
3. **Sigue la guía** específica en `ALTERNATIVAS_DEPLOY.md`

¿Listo para deploy? ¡Vamos! 🚀

