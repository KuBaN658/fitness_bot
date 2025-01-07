from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    """
    Функция, которая устанавливает главное меню бота.

    :param bot: Объект бота, используемый для установки меню.
    """
    # список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/set_profile',
                   description='Настроить свой профиль'),
        BotCommand(command='/log_water',
                   description='Записать выпитую воду'),
        BotCommand(command='/log_food',
                   description='Записать съеденную еду'),
        BotCommand(command='/log_workout',
                   description='Записать длительность тренировки'),
        BotCommand(command='/check_progress',
                   description='Посмотреть прогресс за день'),
    ]
    await bot.set_my_commands(main_menu_commands)
