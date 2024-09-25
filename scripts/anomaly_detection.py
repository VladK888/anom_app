import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

def detect_anomalies():

    # Загрузка данных
    symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']

    def load_data(symbol):
        file_path = f'data/{symbol}_data.csv'
        data = pd.read_csv(file_path)
        return data

    def load_data_2():
        file_path = f'data/News_data.csv'
        news_data = pd.read_csv(file_path)
        return news_data

    # Заголовок приложения
    st.title("Temporal Corridors")

    # Выбор символа
    selected_symbol = st.selectbox("Choose symbol", symbols, key="anomaly_symbol")

    # Загрузка данных
    data = load_data(selected_symbol)
    news_data = load_data_2()

    # Объединение данных
    data = pd.merge(data, news_data, on='Datetime', how='left')

    # Инициализация событий
    data['Event'] = 0
    data['Event_Name'] = None

    # Заполнение событий
    for idx, row in news_data.iterrows():
        event_date = row['Datetime']
        if event_date in data['Datetime'].values:
            data.loc[data['Datetime'] == event_date, 'Event'] = idx + 1
            data.loc[data['Datetime'] == event_date, 'Event_Name'] = row['Event']

    # Визуализация с Plotly
    fig = go.Figure()

    # Добавляем линию закрытия
    fig.add_trace(go.Scatter(
        x=data['Datetime'],
        y=data['close'],
        mode='lines',
        line=dict(color='blue'),
        showlegend=False  # Убираем легенду
    ))

    # Отображаем события с номерами
    for i, row in data[data['Event'] > 0].iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Datetime']],
            y=[row['close']],
            mode='markers+text',
            marker=dict(color='red', size=10),
            text=[str(row['Event'])],  # Отображаем номер события
            textposition="top center",
            showlegend=False  # Убираем легенду
        ))

    # Настройки графика
    fig.update_layout(
        title='Анализ влияния события на цену',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_tickangle=-45,
        hovermode='closest'
    )

    st.plotly_chart(fig)

    # Подготовка таблицы с событиями
    event_info = data[data['Event'] > 0][['Event', 'Event_Name']]
    ###event_info.set_index('Datetime', inplace=True)

    st.write(event_info)

    st.write("Disclaimer")
    st.write(" The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")

