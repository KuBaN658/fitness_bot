from datetime import datetime
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, Bot

from core.tools.users import UserStorage, User
from core.tools.app_logger import get_logger
from core.keyboards.inline import keybord_plots
from core.tools.plots import plot_water, plot_food
from core.tools.diet.diet_food import get_training

# Создаем роутер для обработки базовых команд
basic_router = Router()

logger = get_logger(__name__)


@basic_router.message(Command(commands=['start']))
@basic_router.message(Command(commands=['help']))
async def get_start(message: Message) -> None:
    """
    Обработчик команды /start. Приветствует пользователя и предлагает ввести команду /set_profile.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer(
        'Привет, я фитнес-бот. Я могу расчитывать норму потребления воды и калорий.\r\n' +
        'Для начала вы должны настроить свой профиль. Воспользуйтесь кнопкой menu ' +
        'или введите команду /set_profile. \r\n\r\nЕсли вы уже заполнили профиль, вы можете ' +
        'учитывать количество выпитой воды, количество калорий и треннировки ' +
        'с помощью команд: \r\n/log_water \r\n/log_food \r\n/log_workout \r\n' +
        'Спомощью команды /check_progress вы можете посмотреть прогресс за текущий день.'
    )


@basic_router.message(Command(commands=['check_progress']))
async def check_progress(message: Message) -> None:
    """
    Обработчик команды /check_progress. Показывает прогресс пользователя по воде и калориям.

    :param message: Объект сообщения от пользователя.
    """
    try:
        user: User = UserStorage.get_user(str(message.from_user.id))
    except KeyError:
        logger.error('Пользователь не найден', user_id=message.from_user.id)
        await message.answer(
            'Вы еще не заполнили профиль. Введите команду /set_profile'
            )
        return
    today = str(datetime.now().date())
    if user.burned_water.get(today) is None:
        await user.add_day()
        UserStorage.put_user(user)
    calorie_goal = user.calc_calorie_goal()
    water_goal = await user.calc_water_goal()
    burned_water = sum(user.burned_water[today])
    logged_water = sum(user.logged_water[today])
    day_water = water_goal + burned_water
    remaining_water = day_water - logged_water
    remaining_water = remaining_water if remaining_water > 0 else 0
    logged_calories = sum(user.logged_calories[today])
    burned_calories = sum(user.burned_calories[today])
    await message.answer(
        f'Прогресс:\r\n'
        f'Вода:\r\n'
        f'- Выпито: {logged_water} мл из {day_water}\r\n'
        f'- Осталось {remaining_water} мл воды\r\n'
        f'\r\n'
        f'Калории:\r\n'
        f'- Потреблено: {logged_calories} ккал из {calorie_goal} ккал.\r\n'
        f'- Сожжено: {burned_calories} ккал.\r\n'
        f'- Баланс: {logged_calories - burned_calories} ккал.',
        reply_markup=keybord_plots
    )
    if logged_calories - burned_calories > calorie_goal:
        training = get_training()
        await message.answer(
                f'Вы кушаете больше чем двигаетесь, тренировка: {training} для вас.'
            )


@basic_router.callback_query()
async def plot_graphs(message: Message, bot: Bot) -> None:
    """
    Обработчик команды /plot_water. Показывает график потребления воды за день.

    :param message: Объект сообщения от пользователя.
    """
    if message.data == 'plot_water':
        await message.answer('График потребления воды')
        # Создаем график
        graph = await plot_water(message.from_user.id)

        # Отправляем изображение
        await bot.send_photo(chat_id=message.from_user.id, photo=graph)
    elif message.data == 'plot_food':
        await message.answer('График потребления калорий')
        graph = await plot_food(message.from_user.id)
        await bot.send_photo(chat_id=message.from_user.id, photo=graph)
