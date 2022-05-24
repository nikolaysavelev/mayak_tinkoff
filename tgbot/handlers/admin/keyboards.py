from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import investments_text, github_button_text, secret_level_button_text


def feedback_buttons() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('\U0001F44D', callback_data='+1'),  # \U0001F44D - это палец вверх
        InlineKeyboardButton('\U0001F44E', callback_data='-1'),  # \U0001F44E - это палец вниз
        InlineKeyboardButton('Оставить развёрнутый отзыв', callback_data='-1')
    ]]

    return InlineKeyboardMarkup(buttons)
