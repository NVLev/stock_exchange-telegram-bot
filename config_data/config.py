import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запуск бота"),
    ("help", "Обзор команд"),
    ("dividends", "Дивиденды по акциям")
    # из состояний - кастомные команды
)
API_BASE_URL = "https://iss.moex.com/iss/%s.json"


# 2.  Хелп - "Посмотри, что я могу"
