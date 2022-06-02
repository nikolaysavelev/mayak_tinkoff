from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.handlers.admin.static_text import url


def feedback_buttons() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton('👍', callback_data='positive_answer'),
         InlineKeyboardButton('👎', callback_data='negative_answer')],
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


def buy_button_sma_1():  # TODO можем ли объединить 3 функции в одну?
    buttons = [[InlineKeyboardButton('Купить', callback_data='buy_share', url=f'http://www.tinkoff.ru/invest/stocks/{ticker_sma}?utm_source=mayak_bot&utm_content={user_id}')]]

    return InlineKeyboardMarkup(buttons)
