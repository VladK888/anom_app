import streamlit as st
import pandas as pd
from scripts.preprocessing import preprocess_data,calculate_duration_and_changes
from scripts.investment_sim import investment_simulation
from visualization import plot_price_chart


def main():
    st.title("Protected Application")

    # Простая форма аутентификации
    password = st.text_input("Enter password", type="password")

    if password == "your_password":
        st.write("Welcome to the protected app!")
        # Ваш код для основного приложения
    else:
        st.write("Invalid password")

if __name__ == "__main__":
    main()


# Загрузка данных
file_path = 'data/gold_d.csv'
data = pd.read_csv(file_path)


# Предобработка данных
data = preprocess_data(data)

# Выбор символа
symbols = data['symbol'].unique()
selected_symbol = st.selectbox("Выберите символ", symbols)

# Фильтрация данных по выбранному символу
filtered_data = data[data['symbol'] == selected_symbol]

# Выбор диапазона дат
start_date = st.date_input("Выберите начальную дату", value=filtered_data.index.min())
end_date = st.date_input("Выберите конечную дату", value=filtered_data.index.max())

# Фильтрация данных по выбранному диапазону
filtered_data = filtered_data.loc[start_date:end_date]


# Построение графиков
st.title("Временные Коридоры: Анализ Финансовых Аномалий")
plot_price_chart(filtered_data)



# Симуляция инвестиций
st.header("Симулятор инвестиций")
investment_simulation(filtered_data)



# Рассчитываем среднюю продолжительность
avg_duration_above, avg_duration_below, avg_change_above, avg_change_below= calculate_duration_and_changes(filtered_data)


st.write(f"Средняя продолжительность, когда цена выше обоих МА: {avg_duration_above:.2f} ")
st.write(f"Средняя продолжительность, когда цена ниже обоих МА: {avg_duration_below:.2f} ")

st.write(f"Средний рост, когда цена выше обоих МА: {avg_change_above:.2f} ")
st.write(f"Средний падение, когда цена ниже обоих МА: {avg_change_below:.2f} ")
