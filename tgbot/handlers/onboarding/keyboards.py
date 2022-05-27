from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding import static_text


def make_keyboard_for_strategy() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("Скользящее среднее (SMA)", callback_data='sma')],
        [InlineKeyboardButton("Перепроданность по RSI", callback_data='rsi')]
    ]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_signal() -> InlineKeyboardMarkup:
    #  TODO добавить генератор диплинков + UTM, заменить ссылку гугла
    buttons = [[
        InlineKeyboardButton(static_text.investments_text, url="https://google.com")
    ]]

    return InlineKeyboardMarkup(buttons)
