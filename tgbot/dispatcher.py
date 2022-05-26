"""
    Telegram event handlers
"""
import logging
import sys
from typing import Dict

import telegram.error
from telegram import Bot, Update, BotCommand
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.celery import app  # event processing in async mode
from dtb.settings import TELEGRAM_TOKEN, DEBUG
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.admin.handlers import button, get_feedback
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.utils import files, error


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    dp.add_handler(CommandHandler("strategy", admin_handlers.strategy))
    dp.add_handler(CommandHandler("str_info", admin_handlers.str_info))
    dp.add_handler(CommandHandler("stock", admin_handlers.stock))
    dp.add_handler(CommandHandler("time", admin_handlers.time))
    dp.add_handler(CommandHandler("feedback", admin_handlers.feedback))
    dp.add_handler(CommandHandler("off", admin_handlers.off))

    # broadcast message
    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'),
                       broadcast_handlers.broadcast_command_with_message)
    )
    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # TODO: обратите внимание - здесь обработчик кнопок
    dp.add_handler(CallbackQueryHandler(button))
    # TODO: обратите внимание - здесь сбор сообщений из чата
    dp.add_handler(MessageHandler(Filters.text, get_feedback))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'ru': {
            'strategy': 'Выбрать другую стратегию',
            'str_info': 'Узнать о стратегиях больше️',
            'stock': 'Изменить набор бумаг️',
            'time': 'Настроить удобное время уведомлений',
            'off': 'Выключить сигналы',
            'feedback': 'Оставить фидбэк'
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code='ru',
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
