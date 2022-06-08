import datetime as dt
import os.path
import time
from datetime import datetime

import pandas as pd
from tinkoff.invest import *

from corestrategy.datadownload import token, df_all_figi, df_all_shares, period_of_short_sma, period_of_long_sma


def get_shares_list_to_csv():
    # FUNC позволяет получить из API список всех акций
    # FUNC создаёт CSV-файл c более подробными данными, чем на выходе функции
    # На выход подаётся массив (Series) всех figi акций

    df_figi, df_shares = 'error', 'error'

    try:
        with Client(token) as client:  # обёртка
            all_shares = client.instruments.shares()  # запрашивает название всех акций и закладывает их в переменную
        df_shares = pd.DataFrame(all_shares.instruments)
        df_shares.set_index(['figi'], inplace=True)
        df_figi = df_shares.index  # для подачи на выход функции массива всех figi
        df_shares.to_csv('shares.csv', sep=';')  # выгружает dataframe в CSV
        print('✅Downloaded list of shares')

    except Exception as e:
        print('No internet connection? Reconnecting in 60 sec:')
        print(e)
        time.sleep(60)
        get_shares_list_to_csv()

    return df_figi, df_shares


def get_all_lasts():
    # FUNC поучает на вход массив figi
    # на выходе dataframe со всеми ластами соответствующих figi
    # TODO исключить уточняющие свечи

    with Client(token) as client:
        request_lasts = client.market_data.get_last_prices(
            figi=(df_all_figi.tolist())).last_prices  # запрос данных из API. Отвечает массивом?

    df = pd.DataFrame(columns=['figi', 'last_price', 'datetime'])
    for n in request_lasts:
        last_price = f"{n.price.units}.{n.price.nano // 10000000}"  # парсит last из ответа API
        date_time = dt.datetime(n.time.year, n.time.month, n.time.day, n.time.hour, n.time.minute, n.time.second)
        figi = n.figi  # получает figi из ответа API
        df.loc[len(df.index)] = [figi, last_price, date_time]  # сохраняет данные в DF
    df.set_index('figi', inplace=True)  # индексирует DF по figi

    return df


def sma_cross(actual_short_sma,
              actual_long_sma,
              df_previous_sma_saving,
              figi,
              last_price,
              df_signals,
              ):
    # функция считает, пересекаются ли скользяшки, а далее формирует сигнал
    # вспомогательная функция для def calc_one_signal

    # из DF с SMA берем определенные по figi (SMA предшествуют актуальным)
    previous_short_sma_2 = df_previous_sma_saving.loc[figi].previous_short_sma
    previous_long_sma_2 = df_previous_sma_saving.loc[figi].previous_long_sma

    # математическая проверка на совпадение с условиями сигнала
    crossing_buy = ((actual_short_sma > actual_long_sma) & (previous_short_sma_2 < previous_long_sma_2) & (
            last_price > actual_long_sma))
    crossing_sell = ((actual_short_sma < actual_long_sma) & (previous_short_sma_2 > previous_long_sma_2) & (
            last_price < actual_long_sma))

    ticker = df_all_shares.loc[figi].ticker

    # если условие выполняется, то записываем данные в CSV
    if crossing_sell and df_signals.loc[figi].sell_flag != 1:
        df_one_signal = pd.DataFrame([[figi, ticker, datetime.now(), last_price, 1, 0, 'SMA']],
                                     columns=['figi',
                                              'ticker',
                                              'datetime',
                                              'last_price',
                                              'sell_flag',
                                              'buy_flag',
                                              'strategy_id'])
        df_one_signal.set_index('figi')
        df_signals.append(df_one_signal)  # TODO изменить на concat + test
    if crossing_buy and df_signals.loc[figi].buy_flag != 1:
        df_one_signal = pd.DataFrame([[figi, ticker, datetime.now(), last_price, 0, 1, 'SMA']],
                                     columns=['figi',
                                              'ticker'
                                              'datetime',
                                              'last_price',
                                              'sell_flag',
                                              'buy_flag',
                                              'strategy_id'])
        df_one_signal.set_index('figi')
        df_signals.append(df_one_signal)  # TODO изменить на concat + test


def calc_signal_sma(df_all_lasts, df_previous_sma_saving, n, df_signals):
    # FUNC позволяет распарсить CSV 'SMA' и получить исторические SMA, далее по ластам считает актуальные SMA ежеминутно
    # просчитывает все figi
    # На входе df_all_figi, df_all_historic_sma
    # На выходе актуальные SMA_short, SMA_long, а также SMA_short, SMA_long за минуту назад
    # вспомогательная функция для def calc_signals

    df_all_historic_sma = pd.read_csv('sma.csv', sep=';', index_col=0)
    for figi in df_all_historic_sma.columns[::2]:

        # ниже получаем данные о исторических SMA из CSV
        figi = figi[:12]  # считываем figi без лишних элементов
        df_historic_short_sma = df_all_historic_sma[f'{figi}.short'].dropna()  # подготовка DF с short_SMA по figi

        if df_historic_short_sma.size != 0:  # проверка на пустой DF
            historic_short_sma = df_historic_short_sma.loc[
                df_historic_short_sma.index.max()]  # закладываем в переменную последнюю короткую SMA
        else:
            historic_short_sma = False

        df_historic_long_sma = df_all_historic_sma[f'{figi}.long'].dropna()  # подготовка DF с long_SMA по figi

        if df_historic_long_sma.size != 0:  # проверка на пустой DF
            historic_long_sma = df_historic_long_sma.loc[
                df_historic_long_sma.index.max()]  # закладываем в переменную последнюю длинную SMA
        else:
            historic_long_sma = False

        # ниже получаем актуальные данные о last_price из df_all_lasts и считаем актуальные SMA
        a = datetime.utcnow().year == df_all_lasts.loc[figi].datetime.year
        b = datetime.utcnow().month == df_all_lasts.loc[figi].datetime.month
        c = datetime.utcnow().day == df_all_lasts.loc[figi].datetime.day
        d = datetime.utcnow().hour == df_all_lasts.loc[figi].datetime.hour
        e = datetime.utcnow().minute == df_all_lasts.loc[figi].datetime.minute
        f = datetime.utcnow().minute - 1 == df_all_lasts.loc[figi].datetime.minute
        g = datetime.utcnow().minute - 2 == df_all_lasts.loc[figi].datetime.minute
        h = e or f or g
        if a and b and c and d and h:

            last_price = float(df_all_lasts.loc[figi].last_price)
            if n == 0:
                previous_short_sma = round((
                        (historic_short_sma * (period_of_short_sma - 1) + last_price) / period_of_short_sma), 3)
                previous_long_sma = round((
                        (historic_long_sma * (period_of_long_sma - 1) + last_price) / period_of_long_sma), 3)
                df_previous_sma_saving.loc[figi] = [previous_short_sma, previous_long_sma]

            else:

                actual_short_sma = round((
                        (historic_short_sma * (period_of_short_sma - 1) + last_price) / period_of_short_sma), 3)
                actual_long_sma = round((
                        (historic_long_sma * (period_of_long_sma - 1) + last_price) / period_of_long_sma), 3)
                df_previous_sma_saving.loc[figi] = [actual_short_sma,
                                                 actual_long_sma]  # актуальные сигналы становятся прошлыми

                sma_cross(actual_short_sma, actual_long_sma, df_previous_sma_saving, figi, last_price, df_signals)


def calc_and_save_actual_signals_sma(n):
    # функция позволяет циклически считать сигналы на основе постоянно обновляющихся last_prices

    df_previous_sma_saving = pd.DataFrame(index=df_all_figi, columns=['previous_short_sma', 'previous_long_sma'])
    df_all_lasts = get_all_lasts()
    if not os.path.exists('Actual_signals_SMA.csv'):  # TODO тест переноса из цикла наружу
        df_signals = pd.DataFrame(columns=['figi', "datetime", 'last_price', 'sell_flag', 'buy_flag', 'strategy_id'])
        df_signals.set_index('figi')
    else:
        df_signals = pd.read_csv('Actual_signals_SMA.csv', sep=';', index_col=0)
    calc_signal_sma(df_all_lasts, df_previous_sma_saving, n, df_signals)
    df_signals.to_csv('Actual_signals_SMA.csv', sep=';')
    time.sleep(60)


def run_sma_strategy():
    while True:
        n = 0  # TODO refactor
        if dt.time(hour=4) < datetime.now().time() < dt.time(hour=23):  # время по UTC+0 TODO UTC+3 (docker-настройки)
            print('SMA_strategy_calc_starts')
            calc_and_save_actual_signals_sma(n)
            n += 1  # TODO refactor
        else:
            n = 0  # TODO refactor
            time.sleep(300)
