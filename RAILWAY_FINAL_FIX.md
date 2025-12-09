# Fix Final: Error "cd could not be found" en Railway

## Problema Identificado

Railway está intentando ejecutar el comando `cd backend && gunicorn...` directamente como un ejecutable, no dentro de un shell. Esto causa el error: "The executable `cd` could not be found".

## Solución Aplicada

### 1. Eliminado startCommand de railway.json
- Ya no hay `startCommand` configurado
- Railway usará el `CMD` del Dockerfile directamente

### 2. Dockerfile Configurado Correctamente
- `WORKDIR /app/backend` al final del Dockerfile
- `CMD` usa `/bin/sh -c` para expandir variables de entorno
- **NO usa `cd`** - solo usa `WORKDIR`

### 3. Procfile Opcional
- El Procfile existe pero Railway debería usar el Dockerfile si está presente

## Configuración Final

### Dockerfile
```dockerfile
WORKDIR /app/backend
CMD ["/bin/sh", "-c", "exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120"]
```

### railway.json
```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**NO hay startCommand configurado** - Railway usará el CMD del Dockerfile.

## Verificación en Railway

**IMPORTANTE**: Después de hacer push:

1. Ve a Railway Dashboard → Tu Servicio → Settings
2. Verifica que **NO haya Start Command** configurado manualmente
3. Si hay uno, **ELIMÍNALO completamente**
4. Verifica que Builder sea "DOCKERFILE"
5. Haz un Redeploy

## Por qué Funciona Ahora

- El Dockerfile usa `WORKDIR /app/backend` antes del `CMD`
- El `CMD` no necesita `cd` porque ya estamos en el directorio correcto
- Railway ejecutará el `CMD` del Dockerfile sin intentar usar `cd`
- El formato `/bin/sh -c` permite expandir `${PORT}` correctamente

## Si Aún Falla

Si después de estos cambios sigue fallando:

1. Verifica en Railway Settings que NO haya Start Command
2. Verifica que el Builder sea "DOCKERFILE"
3. Verifica que el Dockerfile esté en la raíz del repositorio
4. Revisa los logs completos del deploy

