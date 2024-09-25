import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def analyzer():
        # Загрузка данных
        symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']
        loaded_data_by_symbol = {}

        # Функция для загрузки данных из CSV
        def load_data(symbol):
            file_path = f'data/{symbol}_data.csv'
            df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
            return df

        # Функция для вычисления изменений и диапазонов для каждого случая
        def calculate_changes_and_ranges_all(df, column_name):
            df['Group'] = (df[column_name] != df[column_name].shift()).cumsum()
            grouped = df[df[column_name]].groupby('Group')

            def calculate_group_changes_and_range(group):
                start_price = group['close'].iloc[0]
                end_price = group['close'].iloc[-1]
                max_price = group['high'].max()
                min_price = group['low'].min()

                absolute_change = end_price - start_price
                percentage_change = (absolute_change / start_price) * 100
                absolute_range = max_price - min_price
                percentage_range = (absolute_range / start_price) * 100

                return pd.Series({
                    'absolute_change': absolute_change,
                    'percentage_change': percentage_change,
                    'absolute_range': absolute_range,
                    'percentage_range': percentage_range
                })

            changes_and_ranges_all = grouped.apply(calculate_group_changes_and_range)
            return changes_and_ranges_all

        # Определяем функции для вычисления изменений и диапазона
        def calculate_changes_and_range(df, column_name):
            df['Group'] = (df[column_name] != df[column_name].shift()).cumsum()
            grouped = df[df[column_name]].groupby('Group')

            def calculate_group_changes_and_range(group):
                start_price = group['close'].iloc[0]
                end_price = group['close'].iloc[-1]
                max_price = group['high'].max()
                min_price = group['low'].min()

                absolute_change = end_price - start_price
                percentage_change = (absolute_change / start_price) * 100
                absolute_range = max_price - min_price
                percentage_range = (absolute_range / start_price) * 100

                return pd.Series({
                    'absolute_change': absolute_change,
                    'percentage_change': percentage_change,
                    'absolute_range': absolute_range,
                    'percentage_range': percentage_range
                })

            changes_and_range = grouped.apply(calculate_group_changes_and_range)
            average_changes_and_range = changes_and_range.mean()

            return average_changes_and_range

        # Функция для подсчета процентов случаев, когда изменения или диапазоны превышают среднее значение
        def calculate_percentage_of_cases_reaching_average(df, avg_value, value_type):
            count_reaching_avg = (df[value_type] >= avg_value).sum()
            total_cases = len(df)
            percentage_reaching_avg = (count_reaching_avg / total_cases) * 100

            return percentage_reaching_avg

        # Заголовок приложения
        st.title("Analyze Finance Data")

        # Выбор символа
        selected_symbol = st.selectbox("Choose symbol", symbols, key="analyzer_symbol")

        # Загрузка данных для выбранного символа
        filtered_data = load_data(selected_symbol)
        st.write(f"Data for {selected_symbol}:")

        # Среднее изменение и диапазон выше и ниже SMA_50
        avg_changes_and_range_above_sma_50 = calculate_changes_and_range(filtered_data, 'Above_SMA_50')
        avg_changes_and_range_below_sma_50 = calculate_changes_and_range(filtered_data, 'Below_SMA_50')

        # Среднее изменение и диапазон выше и ниже SMA_200
        avg_changes_and_range_above_sma_200 = calculate_changes_and_range(filtered_data, 'Above_SMA_200')
        avg_changes_and_range_below_sma_200 = calculate_changes_and_range(filtered_data, 'Below_SMA_200')

        # Шаг 1: Вычисляем все изменения и диапазоны для случаев выше SMA_50
        all_changes_and_ranges_above_sma_50 = calculate_changes_and_ranges_all(filtered_data, 'Above_SMA_50')

        # Шаг 2: Вычисляем все изменения и диапазоны для случаев ниже SMA_50
        all_changes_and_ranges_below_sma_50 = calculate_changes_and_ranges_all(filtered_data, 'Below_SMA_50')

        # Шаг 3: Подсчитываем проценты случаев для каждого показателя, где они превышают средние значения
        # Для случаев выше SMA_50
        percentage_above_sma_50_reaching_absolute_change = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_above_sma_50, avg_changes_and_range_above_sma_50['absolute_change'], 'absolute_change')
        percentage_above_sma_50_reaching_percentage_change = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_above_sma_50, avg_changes_and_range_above_sma_50['percentage_change'], 'percentage_change')
        percentage_above_sma_50_reaching_absolute_range = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_above_sma_50, avg_changes_and_range_above_sma_50['absolute_range'], 'absolute_range')
        percentage_above_sma_50_reaching_percentage_range = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_above_sma_50, avg_changes_and_range_above_sma_50['percentage_range'], 'percentage_range')

        # Для случаев ниже SMA_50
        percentage_below_sma_50_reaching_absolute_change = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_below_sma_50, avg_changes_and_range_below_sma_50['absolute_change'], 'absolute_change')
        percentage_below_sma_50_reaching_percentage_change = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_below_sma_50, avg_changes_and_range_below_sma_50['percentage_change'], 'percentage_change')
        percentage_below_sma_50_reaching_absolute_range = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_below_sma_50, avg_changes_and_range_below_sma_50['absolute_range'], 'absolute_range')
        percentage_below_sma_50_reaching_percentage_range = calculate_percentage_of_cases_reaching_average(all_changes_and_ranges_below_sma_50, avg_changes_and_range_below_sma_50['percentage_range'], 'percentage_range')

        # Визуализация цен и SMA
        st.subheader(f"Chart price and SMA for {selected_symbol}")
        fig, ax = plt.subplots(figsize=(14, 8))

        # График цены закрытия
        ax.plot(filtered_data.index, filtered_data['close'], label='Close price', color='blue')

        # График SMA_50 и SMA_200
        ax.plot(filtered_data.index, filtered_data['SMA_50'], label='SMA 50', color='orange', linestyle='--')
        ax.plot(filtered_data.index, filtered_data['SMA_200'], label='SMA 200', color='green', linestyle='--')

        # Выделение участков, где цена выше или ниже SMA
        ax.fill_between(filtered_data.index, filtered_data['close'], filtered_data['SMA_50'], where=filtered_data['Above_SMA_50'], facecolor='lightgreen', alpha=0.5, label='Above SMA 50')
        ax.fill_between(filtered_data.index, filtered_data['close'], filtered_data['SMA_50'], where=filtered_data['Below_SMA_50'], facecolor='lightcoral', alpha=0.5, label='Below SMA 50')
        ax.fill_between(filtered_data.index, filtered_data['close'], filtered_data['SMA_200'], where=filtered_data['Above_SMA_200'], facecolor='lightblue', alpha=0.5, label='Above SMA 200')
        ax.fill_between(filtered_data.index, filtered_data['close'], filtered_data['SMA_200'], where=filtered_data['Below_SMA_200'], facecolor='lightpink', alpha=0.5, label='Below SMA 200')

        # Настройки графика
        ax.set_title(f'Close price and SMA 50/200 for {selected_symbol}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)

        # Отображение графика в Streamlit
        st.pyplot(fig)

        # Визуализация распределения диапазона
        st.subheader(f"Histogram range price for {selected_symbol}")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_data['range'].dropna(), bins=30, kde=True, color='blue', ax=ax)
        ax.set_xlabel('Average range High - Low (last 200 candles)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Histogram range for {selected_symbol}')
        ax.grid(True)

        # Отображение гистограммы в Streamlit
        st.pyplot(fig)

        # Корреляция закрытых цен и SMA_50
        st.subheader(f"Correlation between price and SMA_200 для {selected_symbol}")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=filtered_data['close'], y=filtered_data['SMA_200'], color='blue', ax=ax)
        ax.set_xlabel('Price close')
        ax.set_ylabel('SMA_50')
        ax.set_title(f'Correlation Price vs SMA_50 for {selected_symbol}')
        ax.grid(True)

        # Отображение корреляционного графика в Streamlit
        st.pyplot(fig)

        # Время нахождения выше/ниже SMA_50
        st.subheader(f"Time spent above and below SMA_200 {selected_symbol}")
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.hist(filtered_data[filtered_data['close'] > filtered_data['SMA_200']]['close'], bins=30, alpha=0.5, label='Above SMA_50')
        plt.hist(filtered_data[filtered_data['close'] <= filtered_data['SMA_200']]['close'], bins=30, alpha=0.5, label='Below SMA_50')
        plt.xlabel('Price close')
        plt.ylabel('Frequency')
        plt.title('Time spent above and below SMA_200')
        plt.legend()
        plt.grid(True)
        st.pyplot(fig)

        # Boxplot визуализация
        st.subheader("Boxplot for Changes and Ranges")
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        sns.boxplot(data=[all_changes_and_ranges_above_sma_50['absolute_change'], all_changes_and_ranges_below_sma_50['absolute_change']], palette="Set2", ax=axs[0, 0])
        axs[0, 0].set_title('Absolute Change')

        sns.boxplot(data=[all_changes_and_ranges_above_sma_50['percentage_change'], all_changes_and_ranges_below_sma_50['percentage_change']], palette="Set2", ax=axs[0, 1])
        axs[0, 1].set_title('Percentage Change')

        sns.boxplot(data=[all_changes_and_ranges_above_sma_50['absolute_range'], all_changes_and_ranges_below_sma_50['absolute_range']], palette="Set2", ax=axs[1, 0])
        axs[1, 0].set_title('Absolute Range')

        sns.boxplot(data=[all_changes_and_ranges_above_sma_50['percentage_range'], all_changes_and_ranges_below_sma_50['percentage_range']], palette="Set2", ax=axs[1, 1])
        axs[1, 1].set_title('Percentage Range')

        plt.tight_layout()

        # Отображение boxplot в Streamlit
        st.pyplot(fig)

        # Добавляем еще один раздел для процентного достижения средних показателей
        st.subheader("Percentage of Averages Achieved for SMA 50 and SMA 200")

        # Данные для визуализации (замените их на реальные значения, рассчитанные ранее в коде)
        categories = ['absolute_change', 'percentage_change', 'absolute_range', 'percentage_range']

        # Проценты случаев для выше SMA_50 и SMA_200
        percentages_above_sma_50_200 = [
            percentage_above_sma_50_reaching_absolute_change,
            percentage_above_sma_50_reaching_percentage_change,
            percentage_above_sma_50_reaching_absolute_range,
            percentage_above_sma_50_reaching_percentage_range
        ]

        # Проценты случаев для ниже SMA_50 и SMA_200
        percentages_below_sma_50_200 = [
            percentage_below_sma_50_reaching_absolute_change,
            percentage_below_sma_50_reaching_percentage_change,
            percentage_below_sma_50_reaching_absolute_range,
            percentage_below_sma_50_reaching_percentage_range
        ]

        # Настройки для гистограммы
        x = np.arange(len(categories))  # Количество категорий для оси X
        width = 0.35  # Ширина столбцов

        # Создание графика
        fig, ax = plt.subplots(figsize=(14, 8))

        # Столбцы для случаев, когда цена выше одновременно SMA_50 и SMA_200
        bars_above = ax.bar(x - width/2, percentages_above_sma_50_200, width, label='Above SMA 50 and SMA 200', color='green')

        # Столбцы для случаев, когда цена ниже одновременно SMA_50 и SMA_200
        bars_below = ax.bar(x + width/2, percentages_below_sma_50_200, width, label='Below SMA 50 and SMA 200', color='red')

        # Настройки осей и меток
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Percentage of Averages Achieved for SMA 50 and SMA 200 (%)')
        ax.set_title('Percentage of Averages Achieved for SMA 50 and SMA 200')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()

        # Добавление значений над столбцами
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}%',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # Смещение текста на 3 единицы вверх
                            textcoords="offset points",
                            ha='center', va='bottom')

        add_labels(bars_above)
        add_labels(bars_below)

        # Показ графика в Streamlit
        st.pyplot(fig)

        st.write("Disclaimer ")
        st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")
