import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def seasonality():
        # Загрузка данных
        symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']

        # Функция для загрузки данных из CSV
        def load_data(symbol):
            file_path = f'data/{symbol}_data.csv'
            df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
            return df

        # Функция для загрузки данных из CSV
        def load_data_2(symbol):
            file_path = f'data/{symbol}_data_D1.csv'
            df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
            return df

        # Заголовок приложения
        st.title("Analyze Finance Data")

        # Выбор символа
        selected_symbol = st.selectbox("Choose symbol", symbols, key="seasonality_symbol")

        # Загрузка данных для выбранного символа
        df = load_data(selected_symbol)
        filtered_data = load_data_2(selected_symbol)


        # Группировка по месяцам для сезонного анализа
        month = filtered_data.groupby('month').agg(
            Diff=('Mean_Diff', 'median'),
            Diff_price=('Max_Mean', 'median'),
            Move=('Max_Min', 'median'),
            SMA_Diff_1=('SMA_Diff_1', 'median'),
            SMA_Diff_2=('SMA_Diff_2', 'median'),
            SMA_Diff_perc_1=('SMA_Diff_Perc_1', 'median'),
            SMA_Diff_perc_2=('SMA_Diff_Perc_2', 'median'),
            Diff_Diff=('Diff_Diff', 'median'),
            Move_min=('Max_Min', 'min'),
            Move_max=('Max_Min', 'max')
        ).reset_index()

        # Визуализация: Столбчатые графики для разных показателей с использованием Plotly
        colors = ['blue', 'orange', 'red', 'green', 'purple']

        fig1 = px.bar(month, x='month', y='Diff', title='Median Difference per Month', color_discrete_sequence=[colors[0]])
        st.plotly_chart(fig1)

        fig2 = px.bar(month, x='month', y='SMA_Diff_1', title='SMA Difference  per Month', color_discrete_sequence=[colors[1]])
        st.plotly_chart(fig2)

        fig3 = px.bar(month, x='month', y='Move', title='Median Max-Min Move per Month', color_discrete_sequence=[colors[2]])
        st.plotly_chart(fig3)

        # Сезонный анализ
        Seasonality = filtered_data.pivot_table(index=['month'], columns='year', values='close')
        Seasonality_normalized = (Seasonality - Seasonality.min()) / (Seasonality.max() - Seasonality.min())
        Seasonality = Seasonality_normalized.reset_index()

        # График сезонности
        seasonality_fig = go.Figure()
        for col in Seasonality.columns:
            if col != 'month':
                seasonality_fig.add_trace(go.Scatter(x=Seasonality['month'], y=Seasonality[col], mode='lines+markers', name=f'Year {col}'))

        seasonality_fig.update_layout(title='Mean Difference over Months', xaxis_title='Month', yaxis_title='Mean Difference')
        st.plotly_chart(seasonality_fig)

        # Добавление столбцов с днем недели и часом
        df['day_of_week'] = df.index.day_name()  # Имя дня недели
        df['hour'] = df.index.hour  # Час

        # Тепловая карта для range_2
        heatmap_data_2 = df.pivot_table(index='hour', columns='day_of_week', values='range_2', aggfunc='median')
        heatmap_data_2 = heatmap_data_2.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

        # Создание тепловой карты с Seaborn
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data_2, cmap='YlGnBu', annot=True, fmt='.2f')
        plt.title('Heatmap of Median Range 2 by Day of Week and Hour')
        plt.xlabel('Day of Week')
        plt.ylabel('Hour')

        # Отображение тепловой карты в Streamlit
        st.pyplot(plt)

        # Тепловая карта для range_3
        heatmap_data_3 = df.pivot_table(index='hour', columns='day_of_week', values='range_3', aggfunc='median')
        heatmap_data_3 = heatmap_data_3.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

        # Создание тепловой карты с Seaborn
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data_3, cmap='YlGnBu', annot=True, fmt='.2f')
        plt.title('Heatmap of Median Up/Down by Day of Week and Hour')
        plt.xlabel('Day of Week')
        plt.ylabel('Hour')

        # Отображение тепловой карты в Streamlit
        st.pyplot(plt)

        st.write("Disclaimer ")
        st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")
