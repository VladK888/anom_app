import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def Moving_Average(data, small_SMA=50, big_SMA=200):
    """
    Симуляция стратегии инвестирования на основе пересечения двух скользящих средних.
    """
    if not pd.api.types.is_datetime64_any_dtype(data.index):
        data.index = pd.to_datetime(data.index)

    data = data.sort_index()

    # Вычисление скользящих средних
    data['SMA_50'] = data['close'].rolling(window=small_SMA).mean()
    data['SMA_200'] = data['close'].rolling(window=big_SMA).mean()

    # Создание столбца сигналов
    data['Signal'] = np.where(data['SMA_50'] > data['SMA_200'], 1, 0)
    data['Position'] = data['Signal'].diff()

    initial_investment = 10000
    position = 0
    balance = initial_investment
    returns = []
    cumulative_returns = []
    buy_signals = []
    sell_signals = []

    # Симуляция
    for i in range(len(data)):
        if data['Position'][i] == 1 and position == 0:  # Покупка
            position = balance / data['close'][i]
            #st.write(f"Bought at {data['close'][i]:.2f} on {data.index[i].strftime('%Y-%m-%d')}")
            buy_signals.append((data.index[i], data['close'][i]))
        elif data['Position'][i] == -1 and position > 0:  # Продажа
            balance = position * data['close'][i]
            #st.write(f"Sold at {data['close'][i]:.2f} on {data.index[i].strftime('%Y-%m-%d')}")
            profit = (balance - initial_investment) / initial_investment * 100
            returns.append(profit)
            sell_signals.append((data.index[i], data['close'][i]))
            position = 0

        cumulative_return = (balance - initial_investment) / initial_investment
        cumulative_returns.append(cumulative_return)

    if position > 0:
        balance = position * data['close'].iloc[-1]
        profit = (balance - initial_investment) / initial_investment * 100
        returns.append(profit)
        cumulative_return = (balance - initial_investment) / initial_investment
        cumulative_returns[-1] = cumulative_return

    total_return = (balance - initial_investment) / initial_investment
    annual_return = (1 + total_return) ** (12 / 3) - 1



    # График
    plt.figure(figsize=(14, 8))
    plt.plot(data.index, data['close'], label='Close Price', color='blue', alpha=0.6)
    plt.plot(data.index, data['SMA_50'], label='SMA 50', color='orange', linestyle='--')
    plt.plot(data.index, data['SMA_200'], label='SMA 200', color='green', linestyle='--')

    if buy_signals:
        buy_dates, buy_prices = zip(*buy_signals)
        plt.scatter(buy_dates, buy_prices, marker='^', color='green', s=100, label='Buy Signal', zorder=5)

    if sell_signals:
        sell_dates, sell_prices = zip(*sell_signals)
        plt.scatter(sell_dates, sell_prices, marker='v', color='red', s=100, label='Sell Signal', zorder=5)

    plt.title('Investment Strategy Simulation (SMA 50/200 Cross)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # График кумулятивной доходности
    plt.figure(figsize=(14, 6))
    plt.plot(data.index, cumulative_returns, label='Cumulative Return', color='purple')
    plt.title('Cumulative Return Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return (%)')
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

    st.write(f"Total Return: {total_return * 100:.2f}%")
    st.write(f"Annual Return: {annual_return * 100:.2f}%")

def Return_Average(data, window=50, z_threshold=2):
    """
    Mean Reversion Strategy based on Z-Score.
    """
    if not pd.api.types.is_datetime64_any_dtype(data.index):
        data.index = pd.to_datetime(data.index)

    data['Moving_Average'] = data['close'].rolling(window=window).mean()
    data['Moving_Std'] = data['close'].rolling(window=window).std()
    data['Z_score'] = (data['close'] - data['Moving_Average']) / data['Moving_Std']

    data['Signal'] = 0
    data['Signal'] = np.where(data['Z_score'] > z_threshold, -1, data['Signal'])
    data['Signal'] = np.where(data['Z_score'] < -z_threshold, 1, data['Signal'])
    data['Position'] = data['Signal'].shift()

    initial_investment = 10000
    position = 0
    balance = initial_investment
    cumulative_returns = []

    for i in range(1, len(data)):
        if data['Position'][i] == 1 and position == 0:  # Покупка
            position = balance / data['close'][i]
            #st.write(f"Bought at {data['close'][i]:.2f} on {data.index[i].strftime('%Y-%m-%d')}")
        elif data['Position'][i] == -1 and position > 0:  # Продажа
            balance = position * data['close'][i]
            #st.write(f"Sold at {data['close'][i]:.2f} on {data.index[i].strftime('%Y-%m-%d')}")
            position = 0
            cumulative_return = (balance - initial_investment) / initial_investment * 100
            cumulative_returns.append(cumulative_return)

    if position > 0:
        balance = position * data['close'].iloc[-1]
        cumulative_return = (balance - initial_investment) / initial_investment * 100
        cumulative_returns.append(cumulative_return)

    total_return = (balance - initial_investment) / initial_investment
    annual_return = (1 + total_return) ** (12 / 3) - 1



    # Построение графиков
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['close'], label='Price', color='blue')
    plt.plot(data.index, data['Moving_Average'], label='Moving Average', color='orange')
    buy_signals = data[data['Position'] == 1]
    sell_signals = data[data['Position'] == -1]
    plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', label='Buy Signal', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', label='Sell Signal', alpha=1)
    plt.title('Price with Buy/Sell Signals')
    plt.legend()

    # График Z-score
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['Z_score'], label='Z-Score', color='purple')
    plt.axhline(z_threshold, color='red', linestyle='--', label='Sell Threshold')
    plt.axhline(-z_threshold, color='green', linestyle='--', label='Buy Threshold')
    plt.title('Z-Score with Buy/Sell Thresholds')
    plt.legend()

    plt.tight_layout()
    st.pyplot(plt)

    # График кумулятивной доходности
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(cumulative_returns)), cumulative_returns, label='Cumulative Returns (%)', color='blue')
    plt.xlabel('Trade')
    plt.ylabel('Cumulative Returns (%)')
    plt.title('Cumulative Returns Over Time')
    plt.legend()
    st.pyplot(plt)

    st.write(f"Total Return: {total_return * 100:.2f}%")
    st.write(f"Annual Return: {annual_return * 100:.2f}%")

def Seasonality_by_hours(df):
    # Проверка наличия необходимых столбцов
    required_columns = ['range_2', 'range_3', 'open', 'close']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Column '{col}' does not exist in the data.")
            return

    # Добавление столбцов с днем недели и часом
    df['day_of_week'] = df.index.day_name()  # Имя дня недели
    df['hour'] = df.index.hour  # Час

    # Тепловая карта для range_2 (волатильность)
    heatmap_data_2 = df.pivot_table(index='hour', columns='day_of_week', values='range_2', aggfunc='median')
    heatmap_data_2 = heatmap_data_2.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

    # Тепловая карта для range_3 (направление сделки)
    heatmap_data_3 = df.pivot_table(index='hour', columns='day_of_week', values='range_3', aggfunc='median')
    heatmap_data_3 = heatmap_data_3.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

    # Сортировка по модулю значений (абсолютные значения) range_3 для выбора топ-10 часов
    heatmap_data_3_abs = heatmap_data_3.abs()
    heatmap_data_3_flat = heatmap_data_3_abs.stack().reset_index()
    heatmap_data_3_flat.columns = ['hour', 'day_of_week', 'abs_range_3']
    top_hours = heatmap_data_3_flat.sort_values(by='abs_range_3', ascending=False).head(10)

    # Принятие решений по топ-10 часам на основе range_3
    signals = []
    for _, row in top_hours.iterrows():
        hour = row['hour']
        day = row['day_of_week']
        range_3_value = heatmap_data_3.loc[hour, day]
        action = 'Buy' if range_3_value > 0 else 'Sell'
        signals.append((hour, day, action))

    # Симуляция стратегии
    initial_investment = 10000
    balance = initial_investment
    trades = []  # Для хранения информации о сделках
    cumulative_returns = []  # Для хранения кумулятивной доходности

    for i, row in df.iterrows():
        # Проверяем, попадает ли текущий час и день в топ-10
        current_hour = row['hour']
        current_day = row['day_of_week']
        signal = next((s for s in signals if s[0] == current_hour and s[1] == current_day), None)

        if signal is not None:
            action = signal[2]
            open_price = row['open']
            close_price = row['close']

            if action == 'Buy':
                # Расчет PnL для покупки
                pnl = close_price - open_price
                trades.append({
                    'Open Time': row.name,
                    'Open Price': open_price,
                    'Close Time': row.name,
                    'Close Price': close_price,
                    'PnL': pnl,
                    'Return (%)': (pnl / initial_investment) * 100
                })

            elif action == 'Sell':
                # Расчет PnL для продажи (шорта)
                pnl = open_price - close_price
                trades.append({
                    'Open Time': row.name,
                    'Open Price': open_price,
                    'Close Time': row.name,
                    'Close Price': close_price,
                    'PnL': pnl,
                    'Return (%)': (pnl / initial_investment) * 100
                })

            # Добавление доходности в кумулятивную доходность
            cumulative_returns.append((pnl / initial_investment) * 100)

    # Преобразование сделок в DataFrame для отображения
    trades_df = pd.DataFrame(trades)

    # Отображение сделок
    #st.write("Trades Summary:")
    #st.dataframe(trades_df)

    # Отображение кумулятивной доходности
    #st.write("Cumulative Returns Over Time:")
    #st.line_chart(cumulative_returns)

    # Визуализация доходности по сделке
    plt.figure(figsize=(12, 6))
    plt.plot(trades_df['Open Time'], trades_df['Return (%)'], marker='o', linestyle='-', color='blue')
    plt.title('Return by Trade')
    plt.xlabel('Trade Open Time')
    plt.ylabel('Return (%)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    st.pyplot(plt)

    # Кумулятивная доходность
    cumulative_returns = np.cumsum(cumulative_returns)
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_returns, marker='o', linestyle='-', color='orange')
    plt.title('Cumulative Returns')
    plt.xlabel('Trade Number')
    plt.ylabel('Cumulative Return (%)')
    plt.grid()
    plt.tight_layout()
    st.pyplot(plt)

    total_return = (sum(trades_df['PnL']) / initial_investment) * 100
    st.write(f"Total Return: {total_return:.2f}%")



def investment_simulation():
    st.title("Investment Strategies Simulation")
    st.sidebar.header("Upload Data")

    # Загрузка данных
    symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']
    loaded_data_by_symbol = {}

    # Функция для загрузки данных из CSV
    def load_data(symbol):
        file_path = f'data/{symbol}_data.csv'
        data = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
        return data  # Убедитесь, что datetime уже установлен как индекс

    # Выбор символа
    selected_symbol = st.selectbox("Choose symbol", symbols, key="analyzer_symbol")

    # Загрузка данных для выбранного символа
    data = load_data(selected_symbol)
    st.write(f"Data for {selected_symbol}:")

    if 'close' in data.columns:
        # Переместили выбор стратегии и параметры ниже выбора символа
        strategy = st.sidebar.selectbox("Select Strategy", ["Moving Average", "Mean Reversion", "Seasonality Analysis"])

        if strategy == "Moving Average":
            Moving_Average(data)
        elif strategy == "Mean Reversion":
            window = st.sidebar.slider("Rolling Window Size", 1, 200, 50)
            z_threshold = st.sidebar.slider("Z-Score Threshold", 0.0, 5.0, 2.0)
            Return_Average(data, window, z_threshold)
        elif strategy == "Seasonality Analysis":
            Seasonality_by_hours(data)
    else:
        st.error("Column 'close' not found in the data.")

    st.write("Disclaimer")
    st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")


