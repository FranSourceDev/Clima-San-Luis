# Fix: Error "The executable `cd` could not be found" en Railway

## Problema
Railway está intentando ejecutar `cd` como un ejecutable directo, lo cual falla porque `cd` es un comando de shell.

## Solución Implementada

El Dockerfile ha sido corregido para:
1. Usar `WORKDIR` para cambiar de directorio (en lugar de `cd`)
2. Usar formato de lista en `CMD` con `sh -c` para ejecutar comandos de shell correctamente

## Verificación en Railway

Si el error persiste, verifica en Railway:

### Opción 1: Usar Dockerfile (Recomendado)
1. Ve a tu proyecto en Railway Dashboard
2. Click en el servicio
3. Ve a **Settings** → **Deploy**
4. Asegúrate de que **"Builder"** esté configurado como **"DOCKERFILE"**
5. Verifica que el **"Dockerfile Path"** sea `Dockerfile`

### Opción 2: Eliminar Procfile temporalmente
Si Railway está intentando usar el Procfile, puedes:
1. Renombrar temporalmente `Procfile` a `Procfile.bak`
2. Hacer commit y push
3. Esto forzará a Railway a usar solo el Dockerfile

### Opción 3: Configurar Start Command en Railway
Si necesitas usar el Procfile:
1. En Railway Settings → Deploy
2. En "Start Command", configura:
   ```
   gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
   ```
3. Asegúrate de que el "Working Directory" sea `/app/backend`

## Dockerfile Actual (Ya Corregido)

El Dockerfile ya tiene:
- `WORKDIR /app/backend` antes del CMD
- `CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} ..."]`

Esto debería funcionar correctamente.

