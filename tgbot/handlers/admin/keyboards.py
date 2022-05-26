from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def feedback_buttons() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton('\U0001F44D', callback_data='positive_answer'),  # \U0001F44D - это палец вверх
         InlineKeyboardButton('\U0001F44E', callback_data='negative_answer')],  # \U0001F44E - это палец вниз
        [InlineKeyboardButton('Оставить развёрнутый отзыв', callback_data='ask_for_feedback')]
    ]
    return InlineKeyboardMarkup(buttons)


def strategy_buttons() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton('Скользящее среднее (SMA)', callback_data='sma')],
               [InlineKeyboardButton('Перепроданность по RSI', callback_data='rsi')]]

    return InlineKeyboardMarkup(buttons)


def stock_buttons() -> InlineKeyboardMarkup:
    buttons = [
               [InlineKeyboardButton('NASDAQ-100', callback_data='NASDAQ-100'),
                InlineKeyboardButton('S&P 500', callback_data='S&P 500')],
               [InlineKeyboardButton('Все акции', callback_data='all_shares')]
    ]

    return InlineKeyboardMarkup(buttons)


def time_button() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton('Без ограничений', callback_data='time_unlimited')]]

    return InlineKeyboardMarkup(buttons)
