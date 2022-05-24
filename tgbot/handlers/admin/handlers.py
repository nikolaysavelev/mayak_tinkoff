from datetime import timedelta

from django.utils.timezone import now
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.admin import static_text
from tgbot.handlers.admin.utils import _get_csv_from_qs_values
from tgbot.models import User

def admin(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins)
        return
    update.message.reply_text(static_text.secret_admin_commands)


def str_info(update: Update, context: CallbackContext) -> None:
    """ Show info about strategies """
    u = User.get_user(update, context)
    update.message.reply_html(static_text.telegraph_1)
    update.message.reply_html(static_text.telegraph_2)


def strategy(update: Update, context: CallbackContext) -> None:
    """ Start strategy """
    # TODO filter signals for user and add to db


def stock(update: Update, context: CallbackContext) -> None:
    """ Filter by stocks """
    # TODO filter stocks for user and add to db


def time(update: Update, context: CallbackContext) -> None:
    """ Edit time for user """
    # TODO edit time for user and add to db


def feedback(update: Update, context: CallbackContext) -> None:
    """ feedback """
    u = User.get_user(update, context)
    update.message.reply_text(static_text.ask_feedback)
    ##
    print(update.message.text)
    # TODO save in the heart and db


def off(update: Update, context: CallbackContext) -> None:
    """ off """
    # TODO filter signals to zero for user and add to db


def stats(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins)
        return

    text = static_text.users_amount_stat.format(
        user_count=User.objects.count(),  # count may be ineffective if there are a lot of users.
        active_24=User.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
    )

    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


def export_users(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins)
        return

    # in values argument you can specify which fields should be returned in output csv
    users = User.objects.all().values()
    csv_users = _get_csv_from_qs_values(users)
    context.bot.send_document(chat_id=u.user_id, document=csv_users)
