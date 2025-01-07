import random


def get_diet_food():
    """
    Возвращает случайное блюдо из файла diet_food.txt.

    :return: Случайное блюдо.
    """
    with open('./core/tools/diet/diet_food.txt', encoding='utf-8') as f:
        food = random.choice(f.readlines()).strip()
    return food


def get_training():
    """
    Возвращает случайную треннировку из trainings.txt.

    :return: случайная тренировка.
    """
    with open('./core/tools/diet/trainings.txt', encoding='utf-8') as f:
        training = random.choice(f.readlines()).strip()
    return training
