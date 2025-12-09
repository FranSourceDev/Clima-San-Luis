# Troubleshooting - Deploy en Railway

## Problemas Comunes y Soluciones

### 1. Build Falla - "Node.js not found" o "npm: command not found"

**Problema**: Railway no detecta que necesita Node.js.

**Solución**: 
- El archivo `nixpacks.toml` debería resolver esto
- Verifica que el archivo esté en la raíz del repositorio
- Si persiste, en Railway Settings → Deploy, verifica que el builder sea "NIXPACKS"

### 2. Build Falla - "Module not found" o errores de dependencias

**Problema**: Faltan dependencias en requirements.txt o package.json.

**Solución**:
- Verifica `backend/requirements.txt` tiene todas las dependencias
- Verifica `frontend/package.json` tiene todas las dependencias
- Revisa los logs del build en Railway para ver qué módulo falta

### 3. Deploy Exitoso pero Frontend no Carga (Error 503)

**Problema**: El frontend no se construyó o la ruta está incorrecta.

**Solución**:
- Verifica en los logs que `npm run build` se ejecutó exitosamente
- Verifica que `frontend/dist/` se creó
- Revisa los logs del runtime para ver errores de Flask

### 4. Error al Iniciar - "gunicorn: command not found"

**Problema**: Gunicorn no está instalado o no está en el PATH.

**Solución**:
- Verifica que `gunicorn==21.2.0` está en `backend/requirements.txt`
- Verifica que el build instaló las dependencias correctamente

### 5. Error - "No module named 'app'"

**Problema**: Gunicorn no encuentra el módulo wsgi.

**Solución**:
- Verifica que `backend/wsgi.py` existe
- Verifica que el startCommand ejecuta desde el directorio `backend/`
- El comando debe ser: `cd backend && gunicorn wsgi:app`

### 6. CORS Errors en el Navegador

**Problema**: Las variables de entorno no están configuradas correctamente.

**Solución**:
- Verifica que `FRONTEND_URL` está configurada en Railway Variables
- Verifica que la URL coincide exactamente (sin barra final)
- Después de cambiar variables, haz un redeploy

### 7. Build Tarda Mucho o Timeout

**Problema**: El build del frontend tarda demasiado.

**Solución**:
- Railway tiene límites de tiempo para builds
- Verifica que `npm ci` (en lugar de `npm install`) esté siendo usado (más rápido)
- Considera optimizar dependencias si es necesario

### 8. Archivo estático no encontrado (404)

**Problema**: Flask no encuentra los archivos en `frontend/dist/`.

**Solución**:
- Verifica que el build creó `frontend/dist/`
- Verifica que la ruta en `app.py` es correcta
- Revisa los logs para ver la ruta absoluta que está usando Flask

## Cómo Revisar Logs en Railway

1. Ve a tu proyecto en Railway Dashboard
2. Click en el servicio
3. Ve a la pestaña **"Deployments"**
4. Click en el deployment que quieres revisar
5. Ve a la sección **"Build Logs"** o **"Deploy Logs"**

## Verificación Paso a Paso

1. **Build Logs**: 
   - ¿Se instalaron las dependencias de Python?
   - ¿Se instalaron las dependencias de Node.js?
   - ¿Se ejecutó `npm run build`?
   - ¿Hay algún error rojo?

2. **Deploy Logs**:
   - ¿Gunicorn inició correctamente?
   - ¿Hay errores de importación?
   - ¿Flask está corriendo?

3. **Variables de Entorno**:
   - ¿Están todas configuradas?
   - ¿Las URLs son correctas?

## Comandos de Debug Local

Para probar localmente antes de deployar:

```bash
# Build del frontend
cd frontend
npm install
npm run build
cd ..

# Probar servidor de producción
cd backend
pip install -r requirements.txt
gunicorn wsgi:app --bind 0.0.0.0:5000
```

Si funciona localmente pero falla en Railway, el problema probablemente está en la configuración de Railway o en las variables de entorno.

## Contactar Soporte

Si el problema persiste:
1. Captura los logs completos del build y deploy
2. Verifica que todos los archivos están en el repositorio
3. Revisa la documentación de Railway: https://docs.railway.app/

