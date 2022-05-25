from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# TODO: remove everything that you never used!

def feedback_buttons() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('\U0001F44D', callback_data='positive_answer'),  # \U0001F44D - это палец вверх
        InlineKeyboardButton('\U0001F44E', callback_data='negative_answer'),  # \U0001F44E - это палец вниз
        # TODO: перенеси на другую строку doc: https://www.programcreek.com/python/example/91611/telebot.types.InlineKeyboardButton
        InlineKeyboardButton('Оставить развёрнутый отзыв', callback_data='ask_for_feedback')
    ]]
    return InlineKeyboardMarkup(buttons)
