from dataclasses import dataclass
from aiogram.fsm.state import State, StatesGroup


@dataclass
class LogFoodForm(StatesGroup):
    """
    Класс для управления состоянием формы логирования съеденного продукта.

    Используется для хранения состояния ввода веса продукта.
    Наследуется от StatesGroup, чтобы определить группу связанных состояний.

    Атрибуты:
        weight (State): Состояние, в котором пользователь вводит вес съеденного продукта.
    """
    weight = State()
