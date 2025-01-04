import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.tools.settings import settings
from core.handlers.basic import basic_router
from core.handlers.form import form_router
from core.tools.users import UserStorage


async def start_bot(bot: Bot) -> None:
    """
    Функция, которая отправляет сообщение администратору при запуске бота.
    Чат с ботом у Администратора должен уже существовать, иначе будет ошибка.

    :param bot: Объект бота, используемый для отправки сообщений.
    """
    await bot.send_message(settings.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot) -> None:
    """
    Функция, которая отправляет сообщение администратору при остановке бота.

    :param bot: Объект бота, используемый для отправки сообщений.
    """
    await bot.send_message(settings.admin_id, text='Бот остановлен!')


async def main() -> None:
    """
    Основная асинхронная функция для запуска бота.

    Инициализирует хранилище пользователей, настраивает диспетчер и запускает бота.
    """
    # Инициализация хранилища пользователей
    UserStorage()

    # Создание диспетчера для обработки сообщений
    dp: Dispatcher = Dispatcher()

    # Подключение роутеров для обработки команд и форм
    dp.include_router(form_router)
    dp.include_router(basic_router)

    # Создание объекта бота с использованием токена из настроек
    bot = Bot(token=settings.bot_token)

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s"
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    # Регистрация функций, которые будут вызваны при запуске и остановке бота
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        # Запуск бота в режиме опроса (polling)
        await dp.start_polling(bot)
    finally:
        # Закрытие сессии бота при завершении работы
        await bot.session.close()

if __name__ == '__main__':
    # Запуск асинхронной функции main() при запуске скрипта
    asyncio.run(main())
