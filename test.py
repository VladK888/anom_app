import streamlit as st
import pandas as pd
from scripts.preprocessing import preprocess_data
from scripts.anomaly_detection import detect_anomalies
from scripts.predictions import arima_model
from scripts.investment_sim import investment_simulation
from visualization import plot_price_chart, plot_volatility, plot_sharpe_ratio

# Загрузка данных
file_path = r"C:\Users\wlad8\financial_anomalies_app\data\XAUUSD.csv"
data = pd.read_csv(file_path)

# Предобработка данных
data = preprocess_data(data)

# Обнаружение аномалий
anomalies = detect_anomalies(data)

print(anomalies)
