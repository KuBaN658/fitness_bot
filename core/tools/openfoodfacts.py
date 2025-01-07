from typing import Dict, Optional
import httpx

from core.tools.app_logger import get_logger

logger = get_logger(__name__)


async def get_food_info(product_name: str) -> Optional[Dict[str, str | int]]:
    """
    Асинхронная функция для получения информации о продукте с помощью API OpenFoodFacts.

    :param product_name: Название продукта, информацию о котором нужно получить.
    :return: Словарь с информацией о продукте, включая название и калории на 100 грамм.
             Если продукт не найден, возвращает словарь с названием продукта и калориями по умолчанию (100).
             В случае ошибки при запросе возвращает None.
    """
    logger.debug('Получение информации о продукте %s', product_name)
    # Формируем URL для запроса к API OpenFoodFacts
    url = (f"https://world.openfoodfacts.org/cgi/search.pl?action="
           f"process&search_terms={product_name}&json=true")
    timeout = httpx.Timeout(30.0)

    # Используем асинхронный HTTP-клиент для выполнения запроса
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=timeout)

        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])

            # Если продукты найдены, берем первый из списка
            if products:
                first_product = products[0]
                return {
                    'name': first_product.get('product_name', 'Неизвестно'),
                    'calories': first_product.get('nutriments', {}).get('energy-kcal_100g', 0)
                }

        # Если продукт не найден, возвращаем данные по умолчанию
        logger.debug('Продукт %s не найден', product_name)
        return {
            'name': product_name,
            'calories': 100
        }

    # В случае ошибки выводим статус код и возвращаем None
    logger.error('Ошибка при получении информации о продукте %s', product_name)
    return None
