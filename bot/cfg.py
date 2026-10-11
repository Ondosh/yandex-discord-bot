import os
from pathlib import Path
from dotenv import load_dotenv

# .env лежит в корне проекта. Уже заданные переменные окружения имеют приоритет.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

token = os.environ["discordBotToken"]
YMToken = os.environ["YMTOKEN"]
