from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from aiogram.types.input_file import FSInputFile
from core.tools.users import UserStorage


async def plot_water(telegram_id: int) -> FSInputFile:
    """
    Создает график потребления воды для пользователя.

    :param telegram_id: Идентификатор пользователя в Telegram.
    :return: Объект FSInputFile с изображением графика.
    """
    # Получаем данные пользователя
    user = UserStorage.get_user(str(telegram_id))
    data = user.model_dump()

    # Получаем текущую дату
    today = str(datetime.now().date())

    # Преобразуем данные о потреблении и сжигании воды в массивы numpy
    log = np.array(list(data['logged_water'][today]))
    burn = np.array(list(data['burned_water'][today]))

    # Рассчитываем цель по воде
    water_goal = await user.calc_water_goal()

    # Создаем график
    fig = plt.figure(figsize=(10, 5))
    plt.step(range(1, 25), (log - burn).cumsum(), label='Потребление воды', linewidth=3)
    plt.axhline(water_goal, color='r', linestyle='--', label='Ваша норма воды')
    plt.legend()
    plt.suptitle('Потребление воды', fontsize=16, fontweight='bold')
    plt.grid()
    plt.xlim(1, 24)
    plt.xlabel("Время")
    plt.ylabel("Выпитая вода(мл)")

    # Сохраняем график в файл
    fig.savefig('./tmp/water.png')

    # Возвращаем файл с графиком
    return FSInputFile('./tmp/water.png')


async def plot_food(telegram_id: int) -> FSInputFile:
    """
    Создает график потребления калорий для пользователя.

    :param telegram_id: Идентификатор пользователя в Telegram.
    :return: Объект FSInputFile с изображением графика.
    """
    # Получаем данные пользователя
    user = UserStorage.get_user(str(telegram_id))
    data = user.model_dump()

    # Получаем текущую дату
    today = str(datetime.now().date())

    # Преобразуем данные о потреблении и сжигании калорий в массивы numpy
    log = np.array(list(data['logged_calories'][today]))
    burn = np.array(list(data['burned_calories'][today]))

    # Рассчитываем цель по калориям
    calories_goal = await user.calc_water_goal()

    # Создаем график
    fig = plt.figure(figsize=(10, 5))
    plt.step(range(1, 25), (log - burn).cumsum(), label='Потребление калорий', linewidth=3, color='g')
    plt.axhline(calories_goal, color='r', linestyle='--', label='Дневная норма калорийности еды')
    plt.legend()
    plt.suptitle('Потребление еды', fontsize=16, fontweight='bold')
    plt.grid()
    plt.xlim(1, 24)
    plt.xlabel("Время")
    plt.ylabel("Потребление еды (ккал)")

    # Сохраняем график в файл
    fig.savefig('./tmp/food.png')

    # Возвращаем файл с графиком
    return FSInputFile('./tmp/food.png')
