from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command

from core.states.profile_form_states import ProfileForm
from core.tools.users import User, UserStorage
from core.tools.app_logger import get_logger

# Создаем роутер
profile_router = Router()

logger = get_logger(__name__)


@profile_router.message(Command(commands=['set_profile']))
async def set_profile(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /set_profile. Начинает процесс заполнения профиля пользователя.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    await message.answer('Привет, введите ваш вес.')
    await state.set_state(ProfileForm.weight)


@profile_router.message(ProfileForm.weight)
async def get_weight(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения веса пользователя. Переводит состояние на следующий шаг — ввод роста.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    try:
        weight = int(message.text)
    except ValueError:
        logger.error('Вес не целое число', user_id=message.from_user.id)
        await message.answer('Вес должен быть целым числом.')
        return
    await state.update_data(weight=weight)
    await message.answer(f'Твой вес: {message.text}\r\nТеперь введите ваш рост.')
    await state.set_state(ProfileForm.height)


@profile_router.message(ProfileForm.height)
async def get_height(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения роста пользователя. Переводит состояние на следующий шаг — ввод возраста.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    try:
        height = int(message.text)
    except ValueError:
        logger.error('Рост не целое число', user_id=message.from_user.id)
        await message.answer('Рост должен быть целым числом.')
        return
    await state.update_data(height=height)
    await message.answer(f'Твой рост: {message.text}\r\nТеперь введите ваш возраст.')
    await state.set_state(ProfileForm.age)


@profile_router.message(ProfileForm.age)
async def get_age(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения возраста пользователя. Переводит состояние на следующий шаг — ввод активности.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    await message.answer(f'Твой возраст: {message.text}\r\n'
                         f'Теперь введите сколько минут активности у вас в день?')
    try:
        age = int(message.text)
    except ValueError:
        logger.error('Возраст не целое число', user_id=message.from_user.id)
        await message.answer('Возраст должен быть целым числом.')
        return
    await state.update_data(age=age)
    await state.set_state(ProfileForm.activity)


@profile_router.message(ProfileForm.activity)
async def get_activity(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения уровня активности пользователя. Переводит состояние на следующий шаг — ввод города.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    await message.answer(f'Твоя активность: {message.text}\r\n'
                         f'В каком городе вы находитесь?')
    try:
        activity = int(message.text)
    except ValueError:
        logger.error('Активность не целое число', user_id=message.from_user.id)
        await message.answer('Активность должна быть целым числом.')
        return
    await state.update_data(activity=activity)
    await state.set_state(ProfileForm.city)


@profile_router.message(ProfileForm.city)
async def get_city(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения города пользователя. Завершает процесс заполнения профиля.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния для управления состоянием пользователя.
    """
    await message.answer(f'Твой город: {message.text}\r\n')
    await state.update_data(city=message.text)
    data = await state.get_data()
    await message.answer(
        f'Введеные вами данные: \r\n'
        f'Вес: {data.get("weight")}\r\n'
        f'Рост: {data.get("height")}\r\n'
        f'Возраст: {data.get("age")}\r\n'
        f'Активность: {data.get("activity")}\r\n'
        f'Город: {data.get("city")}\r\n'
    )

    # Создаем объект пользователя и сохраняем его в хранилище
    user = User(
        telegram_id=message.from_user.id,
        weight=data.get("weight"),
        height=data.get("height"),
        age=data.get("age"),
        activity=data.get("activity"),
        city=data.get("city")
    )
    UserStorage.put_user(user)
    logger.info(
        'Пользователь успешно заполнил профиль weight:%d height:%d age:%d activity:%d city:%s',
        data.get("weight"),
        data.get("height"),
        data.get("age"),
        data.get("activity"),
        data.get("city"),
        user_id=message.from_user.id,
    )
    await message.answer(
        'Вы успешно заполнили профиль. Теперь вы можете воспользоваться командами:\r\n'
        '/log_water для записи выпитой воды \r\n'
        '/log_food для записи въеденной еды\r\n'
        '/log_workout для записи треннировки\r\n'
        '/check_progress для просмотра прогресса'
    )
    await state.clear()
