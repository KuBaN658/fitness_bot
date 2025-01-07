import logging
from typing import Any, Dict, Tuple

# Формат логов, который будет использоваться для всех обработчиков
_log_format = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s"


class CustomAdapter(logging.LoggerAdapter):
    """
    Кастомный адаптер для логгера, который добавляет user_id в сообщение лога.
    """
    def process(self, msg: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Обрабатывает сообщение лога, добавляя user_id в начало сообщения.

        :param msg: Исходное сообщение лога.
        :param kwargs: Дополнительные аргументы, переданные в логгер.
        :return: Кортеж из обработанного сообщения и оставшихся аргументов.
        """
        my_context = kwargs.pop('user_id', self.extra['user_id'])
        return f'id:{my_context} "{msg}"', kwargs


def get_file_handler() -> logging.FileHandler:
    """
    Создает и настраивает обработчик логов для записи в файл.

    :return: Настроенный обработчик логов для файла.
    """
    file_handler = logging.FileHandler("./logs/bot.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler() -> logging.StreamHandler:
    """
    Создает и настраивает обработчик логов для вывода в консоль.

    :return: Настроенный обработчик логов для консоли.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name: str) -> CustomAdapter:
    """
    Создает и настраивает логгер с указанным именем.

    :param name: Имя логгера.
    :return: Настроенный логгер с адаптером для добавления user_id.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    logger = CustomAdapter(logger, {'user_id': None})
    return logger
