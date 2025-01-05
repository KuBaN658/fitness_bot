import httpx
from core.tools.app_logger import get_logger

logger = get_logger(__name__)


async def get_weather(city, api_key):
    """
    Асинхронное получение текущей температуры для указанного города через API OpenWeatherMap.

    Параметры:
        city (str): Название города для запроса.
        api_key (str): API-ключ для доступа к OpenWeatherMap.

    Возвращает:
        dict: Ответ API в формате JSON, если запрос успешен.
        str: Текст ошибки, если запрос не удался.
    """
    logger.debug("Получение текущей температуры для города %s", city)
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
        else:
            logger.error(
                "Ошибка при получении текущей температуры для города %s, status code - %d",
                city,
                response.status_code
            )
            return response.text

        return data
