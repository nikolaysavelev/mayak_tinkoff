import pandas as pd

df_texts = pd.read_csv('csv/static_texts.csv', sep=',')


def signal_pars(df_signals):
    # парсит сигналы из DataFrame, который подаётся на вход.
    # создаёт html для оптравки пользователю
    # сохраняет html в DF

    df_text_signals = pd.DataFrame(columns=['text', 'button_text', 'ticker'])

    for i in range(-1, -4, -1):
        if df_signals.iloc[i].buy_flag == 1 and df_signals.iloc[i].strategy_id == 'sma':
            action = df_texts.signal[1]
            action_2 = df_texts.signal[5]
        elif df_signals.iloc[i].strategy_id == 'sma':
            action = df_texts.signal[0]
            action_2 = df_texts.signal[4]
        elif df_signals.iloc[i].buy_flag == 1 and df_signals.iloc[i].strategy_id == 'rsi':
            action = df_texts.signal[1]
            action_2 = df_texts.signal[2]
        else:
            action = df_texts.signal[0]
            action_2 = df_texts.signal[3]

        ticker = df_signals.iloc[i].ticker
        last_price = df_signals.iloc[i].last_price
        date = df_signals.iloc[i].datetime
        currency = df_signals.iloc[i].currency
        share_name = df_signals.iloc[i].share_name

        signal_text = f"{action}\n" \
                      f"{share_name} (${ticker}) {last_price} {currency}\n" \
                      f"{action_2}\n" \
                      f"🕓{date}"  # TODO заменить месяц на МАЙ вместо 05? Добавить время сигнала,
        # TODO добавить доходность
        buy_button_text = f"Купить <b>{ticker}</b> по <b>{last_price} {currency}<b> в Тинькофф Инвестициях"

        df_text_signals.loc[-i] = [signal_text, buy_button_text, ticker]

    return df_text_signals


sma_strategy_link = df_texts.str_info[0]
rsi_strategy_link = df_texts.str_info[1]
strategy_info = df_texts.strategy_choice[3]  # Сообщение при попытке узнать подробнее о стратегиях
strategy_with_links = (f'{strategy_info}\n'
                       f'\n'
                       f'<a href="{sma_strategy_link}"><b>Среднее скользящее (cross-SMA)</b></a>\n'
                       f'<a href="{rsi_strategy_link}"><b>Перепроданность по RSI</b></a>')

add_new_strategy = df_texts.strategy[0]  # Сообщение при попытке подключить ещё одну стратегию
rsi_chosen = df_texts.menu[0]
sma_chosen = df_texts.menu[1]

# FEEDBACK
ask_feedback = df_texts.feedback[0]
feedback_text = df_texts.feedback[1]
positive_answer = df_texts.feedback[2]
negative_answer = df_texts.feedback[3]
final_answer = df_texts.feedback[4]

# INDEX CHOICE
stock_choice = df_texts.stock_choice[0]
nasdaq100_chosen = df_texts.stock_choice[3]
sp500_chosen = df_texts.stock_choice[4]
all_shares_chosen = df_texts.stock_choice[5]

# TIME SETTING
time_settings = df_texts.time[0]
time_settings_unlimited = df_texts.time[1]

off_signals = df_texts.off_signals[0]

hello = df_texts.hello[1]
hello_2 = df_texts.hello[2]
start_created = (f'{hello}\n'
                 f'\n'
                 f'<a href="{sma_strategy_link}"><b>Среднее скользящее (cross-SMA)</b></a>\n'
                 f'<a href="{rsi_strategy_link}"><b>Перепроданность по RSI</b></a>\n'
                 f'\n'
                 f'{hello_2}')
start_not_created = (f'{hello}\n'
                     f'\n'
                     f'<a href="{sma_strategy_link}"><b>Среднее скользящее (cross-SMA)</b></a>\n'
                     f'<a href="{rsi_strategy_link}"><b>Перепроданность по RSI</b></a>\n'
                     f'\n'
                     f'{hello_2}')
