from tgbot.models import User, Strategy
from pandas import read_csv
from time import sleep
from tgbot.handlers.admin.static_text import signal_pars
from tgbot.handlers.admin.keyboards import buy_button
import os
from tgbot.handlers.broadcast_message.utils import _send_message
import datetime as dt
from datetime import datetime


def run_delivery_boy():
    tg_token = os.getenv("TELEGRAM_TOKEN")
    previous_size_df_sma = 9999999
    previous_size_df_rsi = 9999999
    while True:
        if dt.time(hour=4) < datetime.now().time() < dt.time(hour=23):  # время по UTC+0 TODO UTC+3 (docker-настройки)
            print('delivery_boy runs')
            df_sma = read_csv('historic_signals_sma.csv', sep=';')
            df_rsi = read_csv('historic_signals_rsi.csv', sep=';')
            size_df_sma = df_sma.size
            size_df_rsi = df_rsi.size

            if size_df_sma > previous_size_df_sma:
                user_ids = list(Strategy.objects.filter(strategy_name='sma').values_list('user_id', flat=True))
                # list(User.objects.all().values_list('user_id', flat=True)) TODO delete
                text = signal_pars(df_sma).text[1]
                ticker = signal_pars(df_sma).ticker[1]

                for user_id in user_ids:
                    try:
                        _send_message(text=text,
                                      user_id=user_id,
                                      tg_token=tg_token,
                                      disable_web_page_preview=True,
                                      reply_markup=buy_button(user_id, ticker))

                    except Exception as e:
                        # TODO записать user_id в DB? в случае ошибки отправки
                        print(f"Failed to send message to {user_id}, reason: {e}")
                    sleep(0.4)

            if size_df_rsi > previous_size_df_rsi:
                user_ids = list(Strategy.objects.filter(strategy_name='rsi').values_list('user_id', flat=True))
                text = signal_pars(df_rsi).text[1]
                ticker = signal_pars(df_rsi).ticker[1]

                for user_id in user_ids:
                    try:
                        _send_message(text=text,
                                      user_id=user_id,
                                      tg_token=tg_token,
                                      disable_web_page_preview=True,
                                      reply_markup=buy_button(user_id, ticker))

                    except Exception as e:
                        # TODO записать user_id в DB?
                        print(f"Failed to send message to {user_id}, reason: {e}")
                    sleep(0.4)

            previous_size_df_sma = size_df_sma
            previous_size_df_rsi = size_df_rsi

            sleep(60)
        else:
            sleep(300)
