import pandas as pd

df_texts = pd.read_csv('static_texts.csv', sep=',')

sma_strategy_link = 'https://telegra.ph/Strategiya-Srednee-skolzyashchee-SMA-05-05'
rsi_strategy_link = 'https://telegra.ph/Strategiya-Pereprodannost-po-RSI-05-05'
str_info = df_texts.hello[1]
strategy = df_texts.strategy_choice[0]
ask_feedback = df_texts.feedback[0]
stock_choice = df_texts.stock_choice[0]
time_settings = df_texts.time[0]
off_signals = df_texts.off_signals[0]

