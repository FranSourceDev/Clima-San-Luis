import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URLs
URL_CLIMA = os.getenv("URL_CLIMA", "https://clima.sanluis.gob.ar/")
URL_ESTACION = os.getenv("URL_ESTACION", "https://clima.sanluis.gob.ar/Estacion.aspx?Estacion=20")

# Configuración de ejecución
HORA_EJECUCION = os.getenv("HORA_EJECUCION", "07:00")

# Configuración de notificaciones (opcionales)
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración de requests
REQUEST_TIMEOUT = 30  # segundos
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Configuración de logs
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/clima.log"



