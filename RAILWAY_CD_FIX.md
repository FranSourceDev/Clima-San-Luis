# Configuración para usar comandos con `cd` en Railway

## Cambios Realizados

He configurado el proyecto para que funcione correctamente con comandos que usan `cd`:

### 1. Dockerfile
- Instalado `bash` para asegurar compatibilidad con shell
- CMD configurado con `/bin/sh -c` para permitir comandos de shell
- El comando incluye `cd /app/backend && exec gunicorn...`

### 2. railway.json
- Configurado `startCommand` con: `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`

### 3. Procfile
- Recreado con el comando: `web: cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`

## Cómo Funciona

El Dockerfile ahora usa:
```dockerfile
CMD ["/bin/sh", "-c", "cd /app/backend && exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120"]
```

Esto permite que:
- Railway ejecute comandos con `cd` correctamente
- El Start Command en railway.json funcione
- El Procfile funcione si Railway lo detecta

## Configuración en Railway

Railway ahora puede usar cualquiera de estas opciones:

### Opción 1: Usar Dockerfile (Recomendado)
- Builder: `DOCKERFILE`
- Start Command: **Dejarlo vacío** (el Dockerfile ya tiene el CMD correcto)

### Opción 2: Usar Start Command
- Builder: `DOCKERFILE`
- Start Command: `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`

### Opción 3: Usar Procfile
- Builder: `NIXPACKS` o `DOCKERFILE`
- Railway detectará automáticamente el Procfile

## Verificación

Después del deploy, verifica que:
1. El build se completa exitosamente
2. Gunicorn inicia sin errores
3. No hay errores sobre "cd could not be found"

## Notas

- El Dockerfile ahora soporta comandos con `cd` gracias a `/bin/sh -c`
- Railway puede usar el Start Command, Procfile, o el CMD del Dockerfile
- Todos funcionarán correctamente porque el contenedor tiene bash/sh disponible

