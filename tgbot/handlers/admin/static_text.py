import pandas as pd

df_texts = pd.read_csv('static_texts.csv', sep=',')

telegraph_1 = '<a href="https://telegra.ph/Strategiya-Srednee-skolzyashchee-SMA-05-05"><b>SMA</b></a>'
telegraph_2 = '<a href="https://telegra.ph/Strategiya-Pereprodannost-po-RSI-05-05"><b>RSI</b></a>'
ask_feedback = df_texts.feedback[0]
time_settings = df_texts.time[0]
