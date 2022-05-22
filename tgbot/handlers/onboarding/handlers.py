import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_strategy, make_keyboard_for_signal


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    user_ids = list(User.objects.all().values_list('user_id', flat=True))

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_strategy())


def invest_signal(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    user_ids = list(User.objects.all().values_list('user_id', flat=True))
    text = static_text.start_created.format(first_name=u.first_name)
    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_signal())


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )
