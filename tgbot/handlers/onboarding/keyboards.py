from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import investments_text, github_button_text, secret_level_button_text


def make_keyboard_for_strategy() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(github_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}'),
        InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}')
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_signal() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(investments_text, url="https://google.com")
    ]]

    return InlineKeyboardMarkup(buttons)
