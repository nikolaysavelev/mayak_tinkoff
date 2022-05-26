import pandas as pd

df_texts = pd.read_csv('static_texts.csv', sep=',')

sma_strategy_link = df_texts.str_info[0]
rsi_strategy_link = df_texts.str_info[1]

add_new_strategy = df_texts.strategy[0]  # Сообщение при попытке подключить ещё одну стратегию
rsi_chosen = df_texts.menu[0]
sma_chosen = df_texts.menu[1]


strategy_info = df_texts.strategy_choice[3]  # Сообщение при попытке узнать подробнее о стратегиях

ask_feedback = df_texts.feedback[0]
feedback_text = df_texts.feedback[1]

stock_choice = df_texts.stock_choice[0]
nasdaq100_chosen = df_texts.stock_choice[3]
sp500_chosen = df_texts.stock_choice[4]
all_shares_chosen = f'{df_texts.stock_choice[5]} \U0001F44D'

time_settings = df_texts.time[0]
time_settings_unlimited = f'{df_texts.time[1]} \U0001F44D'

off_signals = df_texts.off_signals[0]


