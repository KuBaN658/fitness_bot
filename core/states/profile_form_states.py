from dataclasses import dataclass
from aiogram.fsm.state import State, StatesGroup


@dataclass
class ProfileForm(StatesGroup):
    """
    Класс для управления состоянием формы заполнения профиля пользователя.

    Используется для хранения состояний ввода данных пользователя, таких как вес, рост, возраст,
    уровень активности и город. Наследуется от StatesGroup, чтобы определить группу связанных состояний.

    Атрибуты:
        weight (State): Состояние, в котором пользователь вводит свой вес.
        height (State): Состояние, в котором пользователь вводит свой рост.
        age (State): Состояние, в котором пользователь вводит свой возраст.
        activity (State): Состояние, в котором пользователь вводит уровень своей активности.
        city (State): Состояние, в котором пользователь вводит свой город.
    """
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
