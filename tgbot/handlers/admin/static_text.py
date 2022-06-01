import pandas as pd

df_texts = pd.read_csv('static_texts.csv', sep=',')
df_signals_sma = pd.read_csv('historic_signals_rsi.csv', sep=';')
df_signals_rsi = pd.read_csv('historic_signals_sma.csv', sep=';')
df_text_signals_sma = pd.DataFrame(columns=['text'])
df_text_signals_rsi = pd.DataFrame(columns=['text'])

for i in range(-1, -4, -1):
    if df_signals_sma.iloc[i].buy_flag == 1:
        action_sma = "🟢 BUY"
    else:
        action_sma = "🔴 SELL"
    ticker_sma = df_signals_sma.iloc[i].ticker
    last_price_sma = df_signals_sma.iloc[i].last_price
    date_sma = df_signals_sma.iloc[i].date
    currency_sma = 'USD'  # TODO Пете добавить в сигналы валюту
    investments_text_sma = f"Купить <b>{ticker_sma}</b> по <b>{last_price_sma} {currency_sma}<b> в Тинькофф Инвестициях"
    signal_text_sma = f"{action_sma}\n" \
                      f"'Name of share' (${ticker_sma}) {last_price_sma} {currency_sma}\n" \
                      f"🔺CROSS-SMA {date_sma}"  # TODO заменить месяц на слово вместо цифр?
    # TODO Пете добавить Name of share
    df_text_signals_sma.loc[i] = signal_text_sma  # TODO изменить индексирование

for i in range(-1, -4, -1):
    if df_signals_rsi.iloc[i].buy_flag == 1:
        action_rsi = "🟢 BUY"
    else:
        action_rsi = "🔴 SELL"
    ticker_rsi = df_signals_rsi.iloc[i].ticker
    last_price_rsi = df_signals_rsi.iloc[i].last_price
    date_rsi = df_signals_rsi.iloc[i].datetime
    currency_rsi = 'USD'  # TODO Пете добавить в сигналы валюту
    investments_text_rsi = f"Купить <b>{ticker_rsi}</b> по <b>{last_price_rsi} {currency_rsi}<b> в Тинькофф Инвестициях"
    signal_text_rsi = f"{action_rsi}\n" \
                      f"'Name of share' (${ticker_rsi}) {last_price_rsi} {currency_rsi}\n" \
                      f"🔺CROSS-SMA {date_rsi}"  # TODO заменить месяц на слово вместо цифр?
    # TODO Пете добавить Name of share
    df_text_signals_rsi.loc[i] = signal_text_rsi  # TODO изменить индексирование

investments_text = "Купить <b>GPC</b> по <b>137,61 USD<b> в Тинькофф Инвестициях"
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

ask_feedback = df_texts.feedback[0]
feedback_text = df_texts.feedback[1]
positive_answer = df_texts.feedback[2]
negative_answer = df_texts.feedback[3]

stock_choice = df_texts.stock_choice[0]
nasdaq100_chosen = df_texts.stock_choice[3]
sp500_chosen = df_texts.stock_choice[4]
all_shares_chosen = df_texts.stock_choice[5]

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
