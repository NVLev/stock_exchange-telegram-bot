import os
from dotenv import load_dotenv, find_dotenv
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = 'chat_database.db'
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "🚀 Запуск бота"),
    ("help", "\U0001F4A1 Обзор команд"),
    ("dividends", "\U0001F4B0 Дивиденды по акциям"),
    ('currency', '🏛️ Курс валют по ЦБ РФ'),
    ('stock', '\U0001F4C8 Котировки акций'),
    ('history', '\U0001F4DC История сообщений')
    # из состояний - кастомные команды
)
API_BASE_URL = "https://iss.moex.com/iss/%s.json"



