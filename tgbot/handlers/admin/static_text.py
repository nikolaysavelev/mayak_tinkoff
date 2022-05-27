import pandas as pd

df_texts = pd.read_csv('static_texts.csv', sep=',')

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
all_shares_chosen = f'{df_texts.stock_choice[5]} 👍'

time_settings = df_texts.time[0]
time_settings_unlimited = f'{df_texts.time[1]} 👍'

off_signals = df_texts.off_signals[0]

start_created = (f'На данный момент я умею работать с двумя стратегиями:\n'
                 f'\n'
                 f'<a href="{sma_strategy_link}"><b>Среднее скользящее (cross-SMA)</b></a>\n'
                 f'<a href="{rsi_strategy_link}"><b>Перепроданность по RSI</b></a>\n'
                 f'\n'
                 f'Давай выберем стратегию! 😎')
start_not_created = (f'На данный момент я умею работать с двумя стратегиями:\n'
                     f'\n'
                     f'<a href="{sma_strategy_link}"><b>Среднее скользящее (cross-SMA)</b></a>\n'
                     f'<a href="{rsi_strategy_link}"><b>Перепроданность по RSI</b></a>\n'
                     f'\n'
                     f'Давай выберем стратегию! 😎')
