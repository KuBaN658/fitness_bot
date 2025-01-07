from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from core.tools.app_logger import get_logger

# Инициализация логгера для текущего модуля
logger = get_logger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware для логирования входящих сообщений.
    Логирует текст сообщения и ID пользователя.
    """
    # pylint: disable=too-few-public-methods
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обрабатывает входящее сообщение, логируя его текст и ID пользователя.

        :param handler: Обработчик, который будет вызван после middleware.
        :param event: Входящее сообщение.
        :param data: Дополнительные данные, переданные в обработчик.
        :return: Результат выполнения обработчика.
        """
        # Логируем текст сообщения и ID пользователя
        logger.info(event.text, user_id=event.from_user.id)

        # Передаем управление обработчику
        return await handler(event, data)
