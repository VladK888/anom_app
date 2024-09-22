import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def detect_anomalies():

        # Загрузка данных
        symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']
        def load_data(symbol):
            file_path = f'data/{symbol}_data.csv'
            data = pd.read_csv(file_path)
            return data

        # Функция для загрузки данных из CSV
        def load_data_2():
            file_path = f'data/News.csv'
            news_data = pd.read_csv(file_path)
            news_data['Datetime'] = pd.to_datetime(news_data['Date'] + ' ' + news_data['Time'])

        # Удаляем дубликаты, оставляя только строки, где все значения NaN
            news_data = news_data[~news_data.duplicated(keep='first', subset=['Event']) |
                                news_data[['Actual', 'Forecast', 'Previous']].notna().any(axis=1)]
            return news_data

                # Заголовок приложения
        st.title("Analysis of Financial Anomalies")

        # Выбор символа
        selected_symbol = st.selectbox("Choose symbol", symbols, key="anomaly_symbol")

        # Загрузка данных
        data = load_data(selected_symbol)
        news_data = load_data_2()
        # Объединение данных
        data = pd.merge(data, news_data, on='Datetime', how='left')

        # Инициализация событий
        data['Event'] = 0  # Изначально 0
        data['Event_Name'] = None  # Изначально None для названий событий

        # Заполнение событий
        for idx, row in news_data.iterrows():
            event_date = row['Datetime']  # Добавлено определение event_date
            if event_date in data['Datetime'].values:
                data.loc[data['Datetime'] == event_date, 'Event'] = idx + 1  # Номер события
                data.loc[data['Datetime'] == event_date, 'Event_Name'] = row['Event']  # Название события


        # Визуализация
        plt.figure(figsize=(12, 6))
        plt.plot(data['Datetime'], data['close'], label='Закрытие', color='blue')

        # Отображаем события с выносными линиями
        for i, row in data[data['Event'] > 0].iterrows():
            plt.scatter(row['Datetime'], row['close'], color='red', zorder=5)  # Точка события

            # Случайный сдвиг для высоты
            random_offset = np.random.randint(20, 50)  # Генерируем случайное значение между 20 и 50
            if i % 2 == 0:  # Четные индексы — линия вверх
                y_offset = random_offset
                text_offset = random_offset + 10  # Немного выше линии
            else:  # Нечетные индексы — линия вниз
                y_offset = -random_offset
                text_offset = -random_offset - 10  # Немного ниже линии

            # Сноска с номером события
            plt.text(row['Datetime'], row['close'] + text_offset, str(row['Event']), color='red', fontsize=10, ha='center', va='bottom' if y_offset > 0 else 'top', rotation=-20)

            # Выносная линия
            plt.plot([row['Datetime'], row['Datetime']], [row['close'], row['close'] + y_offset], color='red', linestyle='--', linewidth=1)

        plt.xlabel('Дата')
        plt.ylabel('Цена')
        plt.title('Анализ влияния события на цену')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)  # Поворот меток по оси X для лучшей читаемости
        plt.tight_layout()

        # Подготовка таблицы с событиями
        event_info = data[data['Event'] > 0][['Datetime', 'Event', 'Event_Name', 'Actual', 'Forecast', 'Previous']]



        event_info.set_index('Datetime', inplace=True)

        st.plt.show()

        st.write(event_info)

        return anomalies
