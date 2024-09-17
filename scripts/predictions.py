from statsmodels.tsa.arima.model import ARIMA
import streamlit as st

def arima_model(data):

    data['close'] = data['close'].dropna()

    # Подготавливаем временной ряд
    model = ARIMA(data['close'], order=(5, 1, 0))

    try:
        # Подгоняем модель
        results = model.fit()  # Удалили метод оптимизации

        st.write(results.summary())

        # Прогноз на следующие 10 периодов
        forecast = results.get_forecast(steps=10).predicted_mean
        st.line_chart(forecast)
    except Exception as e:
        st.error(f"Ошибка в модели ARIMA: {str(e)}")
