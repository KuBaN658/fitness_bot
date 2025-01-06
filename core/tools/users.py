import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from core.tools.openweathermap import get_weather
from core.tools.settings import settings
from core.tools.app_logger import get_logger

logger = get_logger(__name__)


class User(BaseModel):
    """
    Класс для хранения и управления данными пользователя.

    Атрибуты:
        telegram_id (int): Уникальный идентификатор пользователя.
        weight (int): Вес пользователя в килограммах.
        height (int): Рост пользователя в сантиметрах.
        age (int): Возраст пользователя.
        activity (int): Уровень активности пользователя (в минутах активности в день).
        city (str): Город пользователя.
        logged_water (int): Количество выпитой воды в миллилитрах.
        logged_calories (int): Количество потребленных калорий.
        burned_calories (int): Количество сожженных калорий.
        burned_water (int): Дополнительное количество воды, которое нужно выпить из-за активности.
        water_goal (Optional[int]): Дневная норма воды.
        calorie_goal (Optional[int]): Дневная норма калорий.
    """

    telegram_id: int
    weight: int
    height: int
    age: int
    activity: int
    city: str
    logged_water: int = 0
    logged_calories: int = 0
    burned_calories: int = 0
    burned_water: int = 0
    water_goal: Optional[int] = None
    calorie_goal: Optional[int] = None

    async def calc_water_goal(self) -> int:
        """
        Рассчитывает дневную норму потребления воды для пользователя.

        Использует данные о погоде в городе пользователя для корректировки нормы.

        :return: Дневная норма воды в миллилитрах.
        """
        weather = await get_weather(self.city, settings.openweathermap_api_key)
        temp = weather["main"]["temp"]
        water_goal = self.weight * 30 + round(self.activity / 30 * 500)
        water_goal = water_goal + 1000 if temp > 25 else water_goal
        self.water_goal = water_goal
        return water_goal

    def calc_calorie_goal(self) -> int:
        """
        Рассчитывает дневную норму потребления калорий для пользователя.

        :return: Дневная норма калорий.
        """
        calorie_goal = self.weight * 10 + round(6.25 * self.height) - 5 * self.age
        calorie_goal = calorie_goal + round(self.activity / 30 * 300)
        self.calorie_goal = calorie_goal
        return calorie_goal


class UserStorage:
    """
    Класс для хранения и управления данными пользователей в файле JSON.

    Методы:
        put_user: Сохраняет данные пользователя в файл.
        get_user: Получает данные пользователя из файла по его ID.
    """

    def __init__(self):
        """
        Инициализирует хранилище пользователей. Создает файл users.json, если он не существует.
        """
        if not os.path.exists("./data/users.json"):
            os.makedirs("./data")
            with open("./data/users.json", "w", encoding="utf-8") as f:
                json.dump({}, f)

    @staticmethod
    def put_user(user: User) -> None:
        """
        Сохраняет данные пользователя в файл users.json.

        :param user: Объект пользователя, данные которого нужно сохранить.
        """
        with open("./data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        users[str(user.telegram_id)] = user.model_dump()
        with open("./data/users.json", "w", encoding="utf-8") as f:
            json.dump(users, f)

    @staticmethod
    def get_user(telegram_id: str) -> Dict[str, Any]:
        """
        Получает данные пользователя из файла users.json по его ID.

        :param id: Уникальный идентификатор пользователя.
        :return: Словарь с данными пользователя или None, если пользователь не найден.
        """
        with open("./data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        user = users.get(telegram_id)
        if user is None:
            raise KeyError("User not found")
        return User.model_validate(user)
