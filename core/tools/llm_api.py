import json
from typing import Dict
import httpx

from core.tools.settings import settings
from core.tools.app_logger import get_logger

# Инициализация логгера для текущего модуля
logger = get_logger(__name__)


async def get_food_info_llm(food_name: str) -> Dict[str, int]:
    """
    Получает информацию о калорийности продукта с использованием Yandex GPT API.

    :param food_name: Название продукта, для которого нужно получить информацию.
    :return: Словарь с ключом 'calories' и значением калорийности продукта.
             В случае ошибки возвращает калорийность по умолчанию (50).
    """
    # URL для запроса к Yandex GPT API
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.iam_token}"
    }

    # Чтение промпта из JSON-файла
    with open("./core/tools/prompts/prompt.json", "r", encoding='utf-8') as f:
        prompt = f.read()

    # Загрузка промпта в формате JSON
    data = json.loads(prompt)

    # Указание модели и передача названия продукта в промпт
    data['modelUri'] = f"gpt://{settings.folder_id}/yandexgpt"
    data['messages'][1]['text'] = food_name

    # Асинхронный запрос к Yandex GPT API
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    try:
        # Извлечение калорийности из ответа API
        calories = int(response.json()['result']['alternatives'][0]['message']['text'])
    except KeyError:
        # Логирование ошибки, если не удалось извлечь калорийность
        logger.error(response.text)
        calories = 50  # Значение по умолчанию в случае ошибки

    # Возврат результата в виде словаря
    return {"calories": calories}
