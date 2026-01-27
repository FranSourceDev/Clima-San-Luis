# Sistema de Caché y Respaldo - Clima San Luis

## 📋 Descripción

El sistema ahora incluye un mecanismo de **persistencia y respaldo automático** que garantiza la disponibilidad de datos del clima incluso cuando:

- El sitio web de REM está caído o no responde
- La conexión a Internet falla
- El scraping retorna datos vacíos o incompletos

## 🔧 Funcionamiento

### Guardado Automático

Cada vez que el sistema obtiene datos válidos del clima:
1. Valida que los datos contengan información útil (pronóstico o estaciones)
2. Guarda automáticamente estos datos en `/logs/ultimo_clima.json`
3. Incluye un timestamp de cuándo se guardaron los datos

### Recuperación Automática

Cuando ocurre un error o el scraping retorna vacío:
1. El sistema detecta automáticamente la situación
2. Carga los últimos datos guardados del archivo JSON
3. Marca los datos como "usando_cache" = true
4. Retorna los datos guardados sin generar un error

### Validación de Datos

El sistema considera que los datos están vacíos cuando:
- El pronóstico general es nulo o no contiene estado actual ni pronóstico del día
- La lista de estaciones está vacía
- Ambos están vacíos simultáneamente

## 📁 Archivos Modificados

### `src/utils.py`
- **Nueva función**: `guardar_ultimo_clima(clima_data)` - Guarda los datos en JSON
- **Nueva función**: `cargar_ultimo_clima()` - Carga los datos guardados

### `src/scraper.py`
- **Modificado**: `obtener_clima()` - Implementa la lógica de respaldo
  - Valida si los datos scraped son útiles
  - Guarda automáticamente datos válidos
  - Carga el caché cuando hay errores o datos vacíos
  - Agrega campo `usando_cache` para indicar el origen de los datos

### `src/notifier.py`
- **Modificado**: `notificar_consola()` - Muestra aviso cuando se usan datos del caché
- **Modificado**: `notificar_archivo()` - Registra en logs cuando se usan datos del caché

## 🎯 Campos Adicionales en la Respuesta

Los datos del clima ahora incluyen:

```python
{
    'exito': True,
    'usando_cache': False,  # True cuando se cargaron desde el caché
    'timestamp_guardado': '2026-01-27T16:55:45.131951',  # Cuándo se guardó
    'error_original': None,  # El error que causó el uso del caché (si aplica)
    'pronostico_general': {...},
    'estaciones': [...]
}
```

## 🧪 Pruebas

Se incluyen scripts de prueba:

### `test_cache.py`
Verifica que el archivo de caché existe y puede cargarse correctamente.

```bash
source venv/bin/activate
python test_cache.py
```

### `test_cache_fallback.py`
Simula errores y datos vacíos para verificar el respaldo automático.

```bash
source venv/bin/activate
python test_cache_fallback.py
```

## 📊 Ejemplo de Uso

### Scraping Exitoso
```bash
$ python main.py --resumen

==================================================
🌤️  CLIMA SAN LUIS
📅 Martes 27 de Enero de 2026
==================================================
🌤️ Clima San Luis - Martes 27 de Enero de 2026
🌡️ Temperaturas: 17°C - 33°C
🌥️ El cielo está mayormente nublado...
```

### Con Error de Conexión (Usando Caché)
```bash
$ python main.py --resumen

==================================================
🌤️  CLIMA SAN LUIS
📅 Martes 27 de Enero de 2026
⚠️  USANDO DATOS GUARDADOS (última actualización: 27/01/2026 16:55)
==================================================
🌤️ Clima San Luis - Martes 27 de Enero de 2026
🌡️ Temperaturas: 17°C - 33°C
🌥️ El cielo está mayormente nublado...
```

## 🔍 Logs

El sistema registra en los logs:

```
INFO - Datos del clima obtenidos correctamente
INFO - Último clima guardado en /logs/ultimo_clima.json
```

Cuando usa el caché:
```
WARNING - El scraping retornó datos vacíos. Intentando cargar último clima guardado...
INFO - Último clima cargado desde /logs/ultimo_clima.json
INFO - Usando último clima guardado como respaldo
```

## 💡 Ventajas

1. **Alta Disponibilidad**: Los datos están disponibles incluso si el sitio REM falla
2. **Experiencia de Usuario**: No se muestran errores al usuario final
3. **Transparencia**: Se indica claramente cuando se usan datos del caché
4. **Automático**: No requiere configuración adicional
5. **Minimal Impact**: Los datos se guardan solo cuando son válidos

## ⚙️ Configuración

El archivo de caché se guarda en:
```
/logs/ultimo_clima.json
```

No requiere configuración adicional. El sistema funciona automáticamente.

## 🔄 Duración del Caché

- **Backend API**: Usa caché en memoria de 60 segundos (configurable en `backend/routes/api.py`)
- **Archivo persistente**: Se actualiza cada vez que hay datos válidos nuevos
- **Sin expiración**: Los datos guardados no expiran, siempre están disponibles como respaldo

## 📝 Notas

- El primer scraping debe ser exitoso para crear el archivo de caché
- El sistema siempre intenta obtener datos frescos primero
- Solo usa el caché como último recurso
- Los datos del caché incluyen el timestamp de cuándo se guardaron
