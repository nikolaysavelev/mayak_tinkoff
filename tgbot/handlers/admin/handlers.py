from datetime import timedelta  # (used in 'def stats')
from django.utils.timezone import now  # (used in 'def stats')

from telegram import ParseMode, Update  # (parse_mode used in 'def stats')
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.admin import static_text
from tgbot.handlers.admin.keyboards import feedback_buttons, strategy_buttons, stock_buttons, time_button, buy_button
from tgbot.handlers.admin.utils import _get_csv_from_qs_values  # (used in 'def export_users')
from tgbot.models import User, Strategy
from tgbot.handlers.onboarding.handlers import invest_signal  # (used in 'def strategy')

ASK_FOR_FEEDBACK_STATE, GET_FEEDBACK_STATE = range(2)

# TODO удалим ли эту функцию?
#def admin(update: Update, context: CallbackContext) -> None:
#    """ Show help info about all secret admins commands """
#    u = User.get_user(update, context)
#    if not u.is_admin:
#        update.message.reply_text(static_text.only_for_admins)
#        return
#    update.message.reply_text(static_text.secret_admin_commands)


def str_info(update: Update, context: CallbackContext) -> None:
    """ Show info about strategies """
    update.message.reply_html(static_text.strategy_with_links, disable_web_page_preview=True)


def strategy(update: Update, context: CallbackContext) -> None:
    """ Add one more strategy """

    # invest_signal(update, context)
    update.message.reply_text(static_text.add_new_strategy, reply_markup=strategy_buttons())

    # TODO filter signals for user and add to db
    # TODO +скрипт проверки включена ли уже стратегия у юзера


def stock(update: Update, context: CallbackContext) -> None:
    """ Filter by stocks """
    # TODO filter stocks for user and add to db
    buttons = update.message.reply_text(text=static_text.stock_choice, reply_markup=stock_buttons())


def time(update: Update, context: CallbackContext) -> None:
    """ Edit time for user """
    u = User.get_user(update, context)
    buttons = update.message.reply_text(text=static_text.time_settings, reply_markup=time_button())
    # TODO edit time for user and add to db


def feedback(update: Update, context: CallbackContext) -> int:
    """ feedback """
    u = User.get_user(update, context)
    buttons = update.message.reply_text(text=static_text.ask_feedback, reply_markup=feedback_buttons())

    return ASK_FOR_FEEDBACK_STATE


def positive_feedback(update: Update, _) -> int:
    """ Handle thumbs up button then end conversation """
    query = update.callback_query
    query.answer()

    query.edit_message_text(static_text.positive_answer)

    return ConversationHandler.END


def negative_feedback(update: Update, _) -> int:
    """ Handle thumbs down button then ask to write the reason """
    query = update.callback_query
    query.answer()

    query.edit_message_text(static_text.negative_answer)

    return GET_FEEDBACK_STATE


def ask_for_feedback(update: Update, _) -> int:
    """ Handle third button then wait feedback """
    query = update.callback_query
    query.answer()

    query.edit_message_text(static_text.feedback_text)

    return GET_FEEDBACK_STATE


def get_feedback(update: Update, _) -> int:
    """ Collect text then end conversation """
    update.message.reply_text(f"Юля, с днём рождения! Мы тебя любим и очень-очень ценим <3 А вот и твой сюрприз: https://disk.yandex.ru/i/YSgy2SF-sALQjw")  # Спасибо за ваш отзыв! Мы успешно получили ваше сообщение: '{update.message.text}'

    return ConversationHandler.END


def cancel_feedback(update: Update, _) -> int:
    """ cancel feedback process """
    update.message.reply_text('Команда отменена')

    return ConversationHandler.END

# TODO: разбить на разные обработчики
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # This will define which button the user tapped on
    # (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data

    # Now u can define what choice ("callback_data") do what like this:

    if choice == 'rsi':
        update.callback_query.message.reply_html(static_text.rsi_chosen)
        update.callback_query.message.reply_html(static_text.df_text_signals_rsi.loc[1].text[0],
                                                 reply_markup=buy_button())
        update.callback_query.message.reply_html(static_text.df_text_signals_rsi.loc[2].text[0],
                                                 reply_markup=buy_button())
        update.callback_query.message.reply_html(static_text.df_text_signals_rsi.loc[3].text[0],
                                                 reply_markup=buy_button())
        u, created = Strategy.get_strategy_and_created(update, context)
        print(context)
        # TODO: add data to db

    elif choice == 'sma':
        update.callback_query.message.reply_html(static_text.sma_chosen)
        update.callback_query.message.reply_html(static_text.df_text_signals_sma.loc[1].text[0],
                                                 reply_markup=buy_button())
        update.callback_query.message.reply_html(static_text.df_text_signals_sma.loc[2].text[0],
                                                 reply_markup=buy_button())
        update.callback_query.message.reply_html(static_text.df_text_signals_sma.loc[3].text[0],
                                                 reply_markup=buy_button())
        u, created = Strategy.get_strategy_and_created(update, context)
        print(context)
        # TODO: add data to db

    elif choice == 'NASDAQ-100':
        update.callback_query.message.edit_text(static_text.nasdaq100_chosen)
        # TODO: add data to db

    elif choice == 'S&P 500':
        update.callback_query.message.edit_text(static_text.sp500_chosen)
        # TODO: add data to db

    elif choice == 'all_shares':
        update.callback_query.message.edit_text(static_text.all_shares_chosen)
        # TODO: add data to db

    elif choice == 'time_unlimited':
        update.callback_query.message.edit_text(static_text.time_settings_unlimited)
        # TODO: add data to db


def off(update: Update, context: CallbackContext) -> None:
    """ off """
    # update = Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # TODO зачем 4 строки снизу?
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)

    update.message.reply_text(static_text.off_signals)

    # TODO filter signals to zero for user and add to db

# TODO удалим ли эту функцию?
#def stats(update: Update, context: CallbackContext) -> None:
#    """ Show help info about all secret admins commands """
#    u = User.get_user(update, context)
#    if not u.is_admin:
#        update.message.reply_text(static_text.only_for_admins)
#        return
#
#    text = static_text.users_amount_stat.format(
#        user_count=User.objects.count(),  # count may be ineffective if there are a lot of users.
#        active_24=User.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
#    )
#
#    update.message.reply_text(
#        text,
#        parse_mode=ParseMode.HTML,
#        disable_web_page_preview=True,
#    )

# TODO удалим ли эту функцию?
#def export_users(update: Update, context: CallbackContext) -> None:
#    u = User.get_user(update, context)
#    if not u.is_admin:
#        update.message.reply_text(static_text.only_for_admins)
#        return
#
#    # in values argument you can specify which fields should be returned in output csv
#    users = User.objects.all().values()
#    csv_users = _get_csv_from_qs_values(users)
#    context.bot.send_document(chat_id=u.user_id, document=csv_users)
