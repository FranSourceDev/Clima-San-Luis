# Fix: Error "The executable `cd` could not be found" en Railway

## El Problema

Railway está intentando ejecutar un comando que contiene `cd`, pero `cd` no es un ejecutable directo - es un comando de shell.

## Causa Probable

Railway tiene un **"Start Command"** configurado en la UI que está sobrescribiendo el `CMD` del Dockerfile. Este Start Command probablemente contiene:
```
cd backend && gunicorn wsgi:app ...
```

## Solución

### Paso 1: Verificar y Eliminar Start Command en Railway

1. Ve a tu proyecto en [Railway Dashboard](https://railway.app/dashboard)
2. Click en tu servicio
3. Ve a **Settings** (Configuración)
4. Busca la sección **"Deploy"** o **"Service"**
5. Busca el campo **"Start Command"** o **"Command"**
6. **ELIMÍNALO completamente** (déjalo vacío)
7. Guarda los cambios

### Paso 2: Verificar Builder

1. En la misma sección de Settings
2. Verifica que **"Builder"** esté configurado como **"DOCKERFILE"**
3. Si no, cámbialo a **"DOCKERFILE"**

### Paso 3: Verificar que el Dockerfile está en el repositorio

Asegúrate de que el `Dockerfile` esté en la raíz del repositorio y se haya hecho push:
```bash
git add Dockerfile
git commit -m "Add Dockerfile for Railway"
git push
```

### Paso 4: Redeploy

1. Después de eliminar el Start Command
2. Haz click en **"Redeploy"** en Railway
3. O haz un nuevo push al repositorio

## Dockerfile Actual

El Dockerfile ahora usa:
- `WORKDIR /app/backend` - Para establecer el directorio
- `CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT ...` - Sin ningún `cd`

Esto debería funcionar correctamente.

## Verificación

Después del redeploy, verifica los logs. Deberías ver:
- El build completarse exitosamente
- Gunicorn iniciando sin errores
- No debería haber ningún error sobre `cd`

## Si el Problema Persiste

Si después de eliminar el Start Command el problema persiste:

1. **Verifica los logs completos** del deploy
2. **Toma una captura** del error exacto
3. **Verifica** que no haya otros archivos de configuración (Procfile, railway.json, etc.) que puedan estar interfiriendo

## Notas Importantes

- **NO configures un Start Command manual** en Railway cuando uses Dockerfile
- El Dockerfile ya tiene el `CMD` correcto
- Railway usará automáticamente el `CMD` del Dockerfile si no hay Start Command configurado

