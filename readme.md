# Script de Clima Diario - San Luis, Argentina

## 📋 Descripción del Proyecto

Script automatizado en Python que consulta y notifica el clima de San Luis, San Luis, Argentina todos los días a las 7:00 AM desde el sitio oficial de la Red de Estaciones Meteorológicas (REM) del Gobierno de San Luis: **https://clima.sanluis.gob.ar/**

## 🎯 Objetivos

- Obtener información meteorológica actualizada de San Luis, Argentina
- Ejecutar automáticamente todos los días a las 7:00 AM
- Extraer datos del sitio web proporcionado
- Presentar la información de manera clara y útil

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **Scraper Web**: Módulo para extraer datos del sitio web
2. **Scheduler**: Sistema de programación de tareas (cron o Task Scheduler)
3. **Notificador**: Sistema para mostrar/enviar la información del clima
4. **Logger**: Registro de ejecuciones y errores

## 📦 Tecnologías y Librerías

### Librerías Python Requeridas

```
requests==2.31.0
beautifulsoup4==4.12.0
lxml==5.1.0
schedule==1.2.0
python-dotenv==1.0.0
```

### Herramientas de Sistema

- **Linux/Mac**: cron
- **Windows**: Task Scheduler o el propio módulo `schedule` de Python

## 📁 Estructura del Proyecto

```
clima-san-luis/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── scraper.py          # Lógica de web scraping
│   ├── scheduler.py         # Programación de tareas
│   ├── notifier.py          # Sistema de notificaciones
│   └── utils.py             # Funciones auxiliares
│
├── logs/
│   └── .gitkeep
│
├── config/
│   └── settings.py          # Configuraciones
│
└── main.py                  # Script principal
```

## 🔧 Funcionalidades Detalladas

### 1. Scraper Web (`scraper.py`)

**Responsabilidades:**
- Realizar petición HTTP a https://clima.sanluis.gob.ar/
- Parsear HTML con BeautifulSoup
- Extraer información del **Pronóstico General Provincia de San Luis**:
  - Estado del tiempo actual
  - Temperatura mínima y máxima del día
  - Condiciones climáticas (despejado, nublado, lluvia, tormentas)
  - Dirección y velocidad del viento
  - Pronóstico extendido (sábado, domingo, lunes)
  - Informes especiales de alerta si existen
- Opcionalmente: extraer datos de estaciones específicas como "La Punta" o "San Luis Rural"

**Manejo de Errores:**
- Timeout de conexión
- Sitio web no disponible
- Cambios en la estructura HTML del pronóstico
- Validación de datos extraídos

### 2. Scheduler (`scheduler.py`)

**Opciones de Implementación:**

#### Opción A: Usando `schedule` (Python)
```python
import schedule
import time

schedule.every().day.at("07:00").do(obtener_clima)
```

#### Opción B: Usando Cron (Linux/Mac)
```bash
0 7 * * * /usr/bin/python3 /ruta/al/proyecto/main.py
```

#### Opción C: Task Scheduler (Windows)
- Crear tarea programada desde el Panel de Control
- Configurar ejecución diaria a las 7:00 AM

### 3. Notificador (`notifier.py`)

**Opciones de Notificación:**

1. **Consola/Terminal**: Imprimir información
2. **Archivo de texto**: Guardar reporte diario
3. **Email**: Enviar correo electrónico
4. **Telegram Bot**: Mensaje a través de bot
5. **Notificación de escritorio**: Usar `plyer` o `notify-send`

### 4. Logger

- Registro de ejecuciones exitosas
- Registro de errores y excepciones
- Rotación de logs (mantener últimos 30 días)

## 🚀 Instalación y Configuración

### Paso 1: Clonar/Crear el Proyecto

```bash
mkdir clima-san-luis
cd clima-san-luis
```

### Paso 2: Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Crear archivo `.env`:
```
URL_CLIMA=https://clima.sanluis.gob.ar/
URL_ESTACION=https://clima.sanluis.gob.ar/Estacion.aspx?Estacion=20
HORA_EJECUCION=07:00
EMAIL_DESTINO=tu_email@example.com  # Opcional
TELEGRAM_BOT_TOKEN=tu_token  # Opcional
TELEGRAM_CHAT_ID=tu_chat_id  # Opcional
```

### Paso 5: Configurar Programación

#### Linux/Mac (Cron):
```bash
crontab -e
# Agregar:
0 7 * * * /ruta/completa/al/venv/bin/python /ruta/completa/al/main.py
```

#### Windows (Task Scheduler):
1. Abrir Task Scheduler
2. Crear tarea básica
3. Trigger: Diario a las 7:00 AM
4. Action: Iniciar programa python.exe con main.py

## 📝 Ejemplo de Uso

```bash
# Ejecución manual para pruebas
python main.py

# Ejecución continua con schedule
python main.py --daemon
```

## 🔍 Consideraciones Importantes

### Sobre el Sitio Web REM

- **Sitio oficial del Gobierno**: https://clima.sanluis.gob.ar/
- La página principal muestra el pronóstico general de la provincia
- Incluye pronóstico del día actual y extendido (3 días)
- También tiene informes especiales de alerta cuando corresponde
- Datos actualizados de múltiples estaciones meteorológicas
- La estructura HTML es relativamente estable

### Web Scraping Ético

- Es un sitio público del gobierno de San Luis
- Los datos son de acceso abierto
- Implementar delays entre requests (no más de 1 consulta cada 5 segundos)
- No sobrecargar el servidor (1 consulta diaria es apropiada)
- Respetar la disponibilidad del servicio

### Manejo de Errores

- Implementar reintentos (retry) en caso de fallo
- Notificar si el script falla consecutivamente
- Guardar logs para debugging

### Mantenimiento

- El sitio web puede cambiar su estructura
- Actualizar selectores CSS/XPath cuando sea necesario
- Revisar logs periódicamente

## 🧪 Testing

Crear pruebas para:
- Validar parsing de HTML
- Verificar extracción de datos
- Simular diferentes condiciones climáticas
- Probar manejo de errores

## 📊 Mejoras Futuras

1. **Base de Datos**: Almacenar histórico de clima
2. **Gráficos**: Visualizar tendencias de temperatura
3. **Predicción**: Mostrar pronóstico de varios días
4. **API REST**: Exponer datos a otras aplicaciones
5. **Machine Learning**: Predicciones basadas en histórico

## 📄 Licencia

MIT License

## 👤 Autor

Fran

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios.

---

**Nota**: Este proyecto utiliza el sitio oficial de la Red de Estaciones Meteorológicas (REM) del Gobierno de San Luis para obtener datos meteorológicos precisos y actualizados de la provincia.
