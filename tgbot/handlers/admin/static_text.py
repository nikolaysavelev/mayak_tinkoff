import pandas as pd

df_texts = pd.read_csv('static_texts.csv', sep=',')

sma_strategy_link = df_texts.str_info[0]
rsi_strategy_link = df_texts.str_info[1]
str_hello_info = df_texts.hello[1]
strategy_info = df_texts.strategy_choice[3]
ask_feedback = df_texts.feedback[0]
feedback_text = df_texts.feedback[1]
stock_choice = df_texts.stock_choice[0]
time_settings = df_texts.time[0]
off_signals = df_texts.off_signals[0]
time_settings_unlimited = f'{df_texts.time[1]} \U0001F44D'
