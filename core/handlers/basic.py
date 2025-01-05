from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from core.tools.users import UserStorage
from core.tools.app_logger import get_logger

# Создаем роутер для обработки базовых команд
basic_router = Router()

logger = get_logger(__name__)


@basic_router.message(Command(commands=['start']))
async def get_start(message: Message) -> None:
    """
    Обработчик команды /start. Приветствует пользователя и предлагает ввести команду /set_profile.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer(
        'Привет, я фитнес-бот. Я могу расчитывать норму потребления воды и калорий.\r\n' +
        'Для начала работы введи команду /set_profile',
    )


@basic_router.message(Command(commands=['log_water']))
async def log_water(message: Message) -> None:
    """
    Обработчик команды /log_water. Логирует количество выпитой воды.

    :param message: Объект сообщения от пользователя.
    """
    args = message.text.strip().split()

    if len(args) < 2:
        await message.answer('Введите количество воды в мл через пробел.')
        logger.warning('Неверный формат команды.', user_id=message.from_user.id)
        return
    try:
        water = int(args[1])
    except ValueError:
        logger.error('Передано не целое число.', user_id=message.from_user.id)
        await message.answer('Количество воды должно быть целым числом')
    else:
        try:
            user = UserStorage.get_user(str(message.from_user.id))
        except KeyError:
            logger.error('Пользователь не найден', user_id=message.from_user.id)
            await message.answer('Вы еще не заполнили профиль. Введите команду /set_profile')
            return
        user.logged_water += water
        UserStorage.put_user(user)
        await message.answer(f'Вы выпили {water} мл воды')


@basic_router.message(Command(commands=['log_workout']))
async def log_workout(message: Message) -> None:
    """
    Обработчик команды /log_workout. Логирует тренировку и рассчитывает сожженные калории и воду.

    :param message: Объект сообщения от пользователя.
    """
    args = message.text.strip().split()[1:]

    if len(args) != 2:
        await message.answer('Ваша команда должна выглядеть: '
                             '/log_workout <тип тренировки> <количество минут>')
        logger.warning('Неверное количество аргументов', user_id=message.from_user.id)
        return
    type_workout = args[0]
    try:
        duration = int(args[1])
    except ValueError:
        await message.answer('Длительность тренировки должна быть в минутах (целое число)')
        logger.error('Передано не целое число.', user_id=message.from_user.id)
    else:
        try:
            user = UserStorage.get_user(str(message.from_user.id))
        except KeyError:
            logger.error('Пользователь не найден', user_id=message.from_user.id)
            await message.answer('Вы еще не заполнили профиль. Введите команду /set_profile')
            return
        user.burned_calories += duration * 16
        user.burned_water += duration * 10
        UserStorage.put_user(user)
        logger.info('Тренировка записана', user_id=message.from_user.id)
        await message.answer(
            f'{type_workout} {duration} минут - {user.burned_calories} ккал.\r\n'
            f'Дополнительно выпейте {user.burned_water} мл воды.'
        )


@basic_router.message(Command(commands=['check_progress']))
async def check_progress(message: Message) -> None:
    """
    Обработчик команды /check_progress. Показывает прогресс пользователя по воде и калориям.

    :param message: Объект сообщения от пользователя.
    """
    try:
        user = UserStorage.get_user(str(message.from_user.id))
    except KeyError:
        logger.error('Пользователь не найден', user_id=message.from_user.id)
        await message.answer('Вы еще не заполнили профиль. Введите команду /set_profile')
        return
    calorie_goal = user.calc_calorie_goal()
    water_goal = await user.calc_water_goal()
    day_water = water_goal + user.burned_water
    remaining_water = day_water - user.logged_water
    remaining_water = remaining_water if remaining_water > 0 else 0
    await message.answer(
        f'Прогресс:\r\n'
        f'Вода:\r\n'
        f'- Выпито: {user.logged_water} мл из {day_water}\r\n'
        f'- Осталось {remaining_water} мл воды\r\n'
        f'\r\n'
        f'Калории:\r\n'
        f'- Потреблено: {user.logged_calories} ккал из {calorie_goal} ккал.\r\n'
        f'- Сожжено: {user.burned_calories} ккал.\r\n'
        f'- Баланс: {user.logged_calories - user.burned_calories} ккал.'
    )
