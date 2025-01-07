from datetime import datetime
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command

from core.states.log_states import LogFoodForm, LogWaterForm, LogWorkoutForm
from core.tools.users import User, UserStorage
from core.tools.llm_api import get_food_info_llm
from core.tools.app_logger import get_logger
from core.tools.diet.diet_food import get_diet_food

log_router = Router()

logger = get_logger(__name__)


@log_router.message(Command(commands=['log_water']))
async def log_water(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /log_water.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer('Введите количество воды в мл.')
    await state.set_state(LogWaterForm.volume)


@log_router.message(LogWaterForm.volume)
async def log_water_volume(message: Message, state: FSMContext) -> None:
    """
    Логирует количество выпитой воды.

    :param message: Объект сообщения от пользователя.
    """
    try:
        water = int(message.text)
    except ValueError:
        logger.error('Передано не целое число.', user_id=message.from_user.id)
        await message.answer('Количество воды должно быть целым числом')
    else:
        try:
            user: User = UserStorage.get_user(str(message.from_user.id))
        except KeyError:
            logger.error('Пользователь не найден', user_id=message.from_user.id)
            await message.answer('Вы еще не заполнили профиль. Введите команду /set_profile')
            return
        now = datetime.now()
        if user.logged_water.get(str(now.date())) is None:
            await user.add_day()
        user.logged_water[str(now.date())][now.hour] += water
        UserStorage.put_user(user)
        await message.answer(f'Вы выпили {water} мл воды')
        await state.clear()


@log_router.message(Command(commands=['log_food']))
async def log_food(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /log_food.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer('Введите название блюда которое вы съели.')
    await state.set_state(LogFoodForm.name)


@log_router.message(LogFoodForm.name)
async def get_name_food(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает введение продукта который съел пользователь.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    product = message.text
    calories = await get_food_info_llm(product)
    calories = calories.get('calories')
    await message.answer(f'{product} - {calories} ккал на 100г. Сколько грамм вы съели?')
    await state.set_state(LogFoodForm.weight)
    await state.set_data({'product': product, 'calories': calories})


@log_router.message(LogFoodForm.weight)
async def get_weight_food(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения веса съеденного продукта. Логирует калории и завершает процесс.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    data = await state.get_data()
    calories = round(float(data.get('calories')))
    try:
        weight = int(message.text)
    except ValueError:
        logger.error('Вес продукта не целое число', user_id=message.from_user.id)
        await message.answer('Вес продукта должен быть целым числом.')
    user: User = UserStorage.get_user(str(message.from_user.id))
    logged_calories = round(weight / 100 * calories)
    now = datetime.now()
    if user.logged_calories.get(str(now.date())) is None:
        await user.add_day()
    user.logged_calories[str(now.date())][now.hour] += logged_calories
    UserStorage.put_user(user)
    logger.info('Записано калорий: %d', logged_calories, user_id=message.from_user.id)
    await message.answer(f'Записано: {logged_calories} ккал.')
    await state.clear()
    if calories > 200:
        diet_food = get_diet_food()
        await message.answer(
            f'Ты питаешься очень калорийной едой следующий раз съешь лучше - {diet_food}'
            )


@log_router.message(Command(commands=['log_workout']))
async def log_workout(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /log_workout.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    await message.answer('Введите тип тренировки.')
    await state.set_state(LogWorkoutForm.type_workout)


@log_router.message(LogWorkoutForm.type_workout)
async def get_type_workout(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения типа тренировки.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    type_workout = message.text
    await message.answer('Введите длительность тренировки в минутах.')
    await state.set_state(LogWorkoutForm.duration)
    await state.set_data({'type_workout': type_workout})


@log_router.message(LogWorkoutForm.duration)
async def get_duration_workout(message: Message, state: FSMContext) -> None:
    """
    Логирует тренировку и рассчитывает сожженные калории и воду.

    :param message: Объект сообщения от пользователя.
    """
    try:
        duration = int(message.text)
    except ValueError:
        await message.answer('Длительность тренировки должна быть в минутах (целое число)')
        logger.error('Передано не целое число.', user_id=message.from_user.id)
    else:
        try:
            user: User = UserStorage.get_user(str(message.from_user.id))
        except KeyError:
            logger.error('Пользователь не найден', user_id=message.from_user.id)
            await message.answer('Вы еще не заполнили профиль. Введите команду /set_profile')
            return
        now = datetime.now()
        if user.burned_calories.get(str(now.date())) is None:
            await user.add_day()
        user.burned_calories[str(now.date())][now.hour] += duration * 16
        user.burned_water[str(now.date())][now.hour] += duration * 10
        UserStorage.put_user(user)
        logger.info('Тренировка записана', user_id=message.from_user.id)
        data = await state.get_data()
        type_workout = data.get('type_workout')
        await message.answer(
            f'{type_workout} {duration} минут - {duration * 16} ккал.\r\n'
            f'Дополнительно выпейте {duration * 10} мл воды.'
        )
        await state.clear()
