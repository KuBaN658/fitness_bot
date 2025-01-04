import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


@dataclass
class Settings:
    """
    Класс для хранения настроек приложения.

    Используется для централизованного хранения конфигурационных данных, таких как токен бота,
    ID администратора и API-ключ для сервиса OpenWeatherMap.

    Атрибуты:
        bot_token (str): Токен для доступа к Telegram Bot API.
        admin_id (int): ID администратора бота.
        openweathermap_api_key (str): API-ключ для доступа к сервису OpenWeatherMap.
    """
    bot_token: str
    admin_id: int
    openweathermap_api_key: str


# Создаем экземпляр класса Settings, используя переменные окружения
settings = Settings(
    bot_token=os.getenv("BOT_TOKEN"),
    admin_id=int(os.getenv("ADMIN_ID")),
    openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY"),
)
