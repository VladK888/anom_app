import pandas as pd

import pandas as pd
import numpy as np


def main():
    st.title("Protected Application")

    # Простая форма аутентификации
    password = st.text_input("Enter password", type="password")

    if password == "money":
        st.write("Welcome to the protected app!")
        # Ваш код для основного приложения
    else:
        st.write("Invalid password")



def preprocess_data(data):
    # Преобразуем столбец 'close' в числовой формат, заменяя нечисловые значения на NaN
    data['close'] = pd.to_numeric(data['close'], errors='coerce')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')


    # Рассчитываем доходности
    data['Returns'] = data['close'].pct_change(fill_method=None).fillna(0)

    # Вычисляем необходимые метрики

        # Вычисляем 22-дневную и 66-дневную скользящие средние
    data['MA22'] = data['close'].rolling(window=22).mean()
    data['MA66'] = data['close'].rolling(window=66).mean()

    data['Volatility'] = data['close'].rolling(window=66).std()
    data['Sharpe Ratio'] = data['Returns'].rolling(window=66).mean() / data['Returns'].rolling(window=66).std()
    data['22-Day Difference'] = data['high'].rolling(window=66).mean() - data['low'].rolling(window=66).mean()
    data['Z-Score'] = (data['close'] - data['close'].rolling(window=66).mean()) / data['close'].rolling(window=66).std()


    return data


def calculate_adx(data, window=66):
    # Calculate True Range (TR)
    data['prev_close'] = data['close'].shift(1)
    data['TR'] = np.maximum(data['high'] - data['low'],
                            np.maximum(np.abs(data['high'] - data['prev_close']),
                                       np.abs(data['low'] - data['prev_close'])))
    # Calculate Directional Movement (DM)
    data['DM_plus'] = np.where((data['high'] - data['high'].shift(1)) > (data['low'].shift(1) - data['low']),
                               np.maximum(data['high'] - data['high'].shift(1), 0), 0)
    data['DM_minus'] = np.where((data['low'].shift(1) - data['low']) > (data['high'] - data['high'].shift(1)),
                                np.maximum(data['low'].shift(1) - data['low'], 0), 0)

    # Smooth the DM and TR values
    data['TR_smooth'] = data['TR'].rolling(window=window).sum()
    data['DM_plus_smooth'] = data['DM_plus'].rolling(window=window).sum()
    data['DM_minus_smooth'] = data['DM_minus'].rolling(window=window).sum()

    # Calculate Directional Indicators
    data['DI_plus'] = 100 * (data['DM_plus_smooth'] / data['TR_smooth'])
    data['DI_minus'] = 100 * (data['DM_minus_smooth'] / data['TR_smooth'])

    # Calculate ADX
    data['DX'] = 100 * (np.abs(data['DI_plus'] - data['DI_minus']) / (data['DI_plus'] + data['DI_minus']))
    data['ADX'] = data['DX'].rolling(window=window).mean()

    return data



def calculate_duration_and_changes(data):
    data['Above_Both_MA'] = (data['close'] > data['MA22']) & (data['close'] > data['MA66'])
    data['Below_Both_MA'] = (data['close'] < data['MA22']) & (data['close'] < data['MA66'])

    periods_above = data['Above_Both_MA'].astype(int).groupby(data['Above_Both_MA'].ne(data['Above_Both_MA'].shift()).cumsum()).cumsum()
    periods_below = data['Below_Both_MA'].astype(int).groupby(data['Below_Both_MA'].ne(data['Below_Both_MA'].shift()).cumsum()).cumsum()

    avg_duration_above = periods_above.groupby(periods_above).count().mean()
    avg_duration_below = periods_below.groupby(periods_below).count().mean()

    avg_change_above = data.loc[data['Above_Both_MA'], 'close'].pct_change().mean()
    avg_change_below = data.loc[data['Below_Both_MA'], 'close'].pct_change().mean()

    return avg_duration_above, avg_duration_below, avg_change_above, avg_change_below
