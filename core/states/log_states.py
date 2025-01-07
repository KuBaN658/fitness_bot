from dataclasses import dataclass
from aiogram.fsm.state import State, StatesGroup


@dataclass
class LogFoodForm(StatesGroup):
    """
    Класс для управления состоянием формы логирования съеденного продукта.

    Атрибуты:
        name (State): Состояние, в котором пользователь выбирает продукт для логирования.
        weight (State): Состояние, в котором пользователь вводит вес съеденного продукта.
    """
    name = State()
    weight = State()


@dataclass
class LogWaterForm(StatesGroup):
    """
        Класс для управления состоянием формы логирования выпитой воды.

    Атрибуты:
        volume (State): Состояние, в котором пользователь вводит объем выпитой воды.
    """
    volume = State()


@dataclass
class LogWorkoutForm(StatesGroup):
    """
        Класс для управления состоянием формы логирования тренировок.

    Атрибуты:
        type_workout (State): Состояние, в котором пользователь выбирает тип тренировки.
        duration (State): Состояние, в котором пользователь вводит длительность тренировки (в минутах).
    """
    type_workout = State()
    duration = State()
