from datetime import timedelta

from django.utils.timezone import now
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.admin import static_text
from tgbot.handlers.admin.keyboards import feedback_buttons
from tgbot.handlers.admin.utils import _get_csv_from_qs_values
from tgbot.handlers.broadcast_message.static_text import feedback_text
from tgbot.handlers.onboarding.handlers import invest_signal
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
    update.message.reply_html(static_text.telegraph_1)
    update.message.reply_html(static_text.telegraph_2)


def strategy(update: Update, context: CallbackContext) -> None:
    """ Start strategy """

    # TODO: remove, test
    invest_signal(update, context)

    # TODO filter signals for user and add to db


def stock(update: Update, context: CallbackContext) -> None:
    """ Filter by stocks """
    # TODO filter stocks for user and add to db


def time(update: Update, context: CallbackContext) -> None:
    """ Edit time for user """
    u = User.get_user(update, context)
    update.message.reply_text(static_text.time_settings)
    # TODO edit time for user and add to db


def feedback(update: Update, context: CallbackContext) -> None:
    """ feedback """
    u = User.get_user(update, context)
    BUTTONS = update.message.reply_text(text=static_text.ask_feedback, reply_markup=feedback_buttons())
    print(BUTTONS)

    # TODO посмотрите что добавило в handlers для обработки колбэка + gjzdbkfcm функция button
    ##
    User.get_user(update, context)

    print(update.message.text)
    # TODO save in the heart and db

def get_feedback(update: Update, context: CallbackContext) -> None:
    # TODO: DONE get user text
    feedback_text = update.message.text
    update.message.reply_text(f"comments: {update.message.text}")

    update.message.reply_text(feedback_text)
    print(feedback_text)
    # TODO: проверить - фидбэк ли это(протащить стейт) и если да - записать в DB

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data

    # Now u can define what choice ("callback_data") do what like this:
    if choice == 'positive_answer':
        print('111')
        # TODO: add to DB

    elif choice == 'negative_answer':
        print('----')
        # TODO: add to DB

    elif choice == 'ask_for_feedback':
        print('feedback requested')
        # TODO: DONE ask for reply
        update.callback_query.message.edit_text(feedback_text)



def off(update: Update, context: CallbackContext) -> None:
    """ off """
    # update = Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)

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
