# Fix: Error de Conexión en Render

## Problema
El frontend muestra: "Error al conectar con el servidor. Asegúrate de que el backend está corriendo."

## Causa
El frontend se construyó con la URL `http://localhost:5000/api` porque `VITE_API_URL` no estaba disponible durante el build, o está intentando conectarse a una URL incorrecta.

## Solución Aplicada

### 1. Cambio en Dashboard.jsx
Ahora el frontend:
- Usa URL relativa (`/api`) cuando está en producción (no localhost)
- Usa `VITE_API_URL` si está configurada
- Solo usa `localhost` en desarrollo local

### 2. Pasos para Aplicar el Fix

1. **Haz commit y push del cambio**:
```bash
git add frontend/src/components/Dashboard.jsx
git commit -m "Fix: Use relative API URL in production"
git push
```

2. **En Render Dashboard**:
   - Ve a tu servicio
   - Ve a la pestaña **"Manual Deploy"**
   - Click en **"Clear build cache & deploy"** para reconstruir el frontend

3. **Verifica las variables de entorno** en Render:
   - Ve a **Environment**
   - Asegúrate de tener:
     - `FLASK_ENV` = `production`
     - `FRONTEND_URL` = `https://tu-url.onrender.com` (tu URL real)
     - `VITE_API_URL` = `https://tu-url.onrender.com/api` (opcional, ya no es necesario)

## Verificación

Después del redeploy:

1. **Verifica que el build incluyó el cambio**:
   - Revisa los logs del build en Render
   - Debe mostrar que se construyó el frontend

2. **Abre la consola del navegador** (F12):
   - Ve a la pestaña "Network"
   - Recarga la página
   - Verifica que las peticiones vayan a `/api/...` (URL relativa)
   - No deben ir a `http://localhost:5000/api`

3. **Verifica que funcionan los endpoints**:
   - `/api/health` debe retornar `{"status":"ok"}`
   - `/api/estaciones` debe retornar datos
   - `/api/clima` debe retornar datos

## Si Aún No Funciona

### Verificar CORS:
El backend debe permitir el dominio de Render. Verifica que:
- `FRONTEND_URL` en Render apunta a tu URL real de Render
- El backend está usando esa URL para CORS

### Verificar que el backend está corriendo:
1. Ve a los **Logs** de Render
2. Verifica que gunicorn está corriendo
3. Busca errores en los logs

### Verificar rutas:
1. Visita directamente: `https://tu-url.onrender.com/api/health`
2. Debe retornar `{"status":"ok"}`
3. Si no funciona, el backend no está corriendo correctamente

## Debug Adicional

Si el problema persiste, verifica en la consola del navegador:
1. Abre DevTools (F12)
2. Ve a la pestaña "Console"
3. Busca errores de red o CORS
4. Ve a "Network" y verifica:
   - ¿Las peticiones van a la URL correcta?
   - ¿Hay errores 404, 500, o CORS?

## Contacto

Si nada funciona:
1. Comparte los logs de Render (build y runtime)
2. Comparte los errores de la consola del navegador
3. Verifica que `/api/health` funciona directamente

