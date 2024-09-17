import streamlit as st

def investment_simulation(data):
    st.write("Введите начальную сумму инвестиций:")
    # Ensure all numerical values are of the same type (float)
    initial_amount = st.number_input("Начальная сумма", value=1000.0, min_value=0.0, step=0.01)

    st.write("Выберите стратегию (консервативная, агрессивная):")
    strategy = st.selectbox("Стратегия", ["Консервативная", "Агрессивная"])

    # Параметры стратегии
    volatility_threshold = st.slider("Порог волатильности", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
    zscore_threshold = st.slider("Порог Z-Score", min_value=-3.0, max_value=3.0, value=2.0, step=0.1)
    adx_threshold = st.slider("Порог ADX", min_value=0, max_value=100, value=25, step=1)

    # Инициализация переменных для симуляции
    cash = initial_amount
    position = 0
    entry_price = 0

    for i in range(1, len(data)):
        # Проверяем торговые сигналы
        if strategy == "Агрессивная":
            # Покупка, если Z-Score ниже порога и ADX выше порога
            if data['Z-Score'].iloc[i] < -zscore_threshold and data['ADX'].iloc[i] > adx_threshold and cash > 0:
                position = cash / data['close'].iloc[i]
                cash = 0
                entry_price = data['close'].iloc[i]

            # Продажа, если Z-Score выше порога и ADX ниже порога
            elif data['Z-Score'].iloc[i] > zscore_threshold and data['ADX'].iloc[i] < adx_threshold and position > 0:
                cash = position * data['close'].iloc[i]
                position = 0

        else:
            # Консервативная стратегия
            # Покупка, если волатильность выше порога и ADX выше порога
            if data['Volatility'].iloc[i] > volatility_threshold and data['ADX'].iloc[i] > adx_threshold and cash > 0:
                position = cash / data['close'].iloc[i]
                cash = 0
                entry_price = data['close'].iloc[i]

            # Продажа, если волатильность ниже порога и ADX ниже порога
            elif data['Volatility'].iloc[i] < volatility_threshold and data['ADX'].iloc[i] < adx_threshold and position > 0:
                cash = position * data['close'].iloc[i]
                position = 0

    # Закрываем последнюю открытую позицию
    if position > 0:
        cash = position * data['close'].iloc[-1]

    final_amount = cash
    st.write(f"Конечная сумма через период: {final_amount:.2f}")
