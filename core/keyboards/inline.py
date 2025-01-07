from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Создание клавиатуры с кнопками для выбора графиков
keybord_plots: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Показать график потребления воды",
                callback_data="plot_water"
            )
        ],
        [
            InlineKeyboardButton(
                text="Показать график потребления еды",
                callback_data="plot_food"
            )
        ]
    ]
)
