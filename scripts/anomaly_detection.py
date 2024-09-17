import pandas as pd

def detect_anomalies(data):
    # Простой пример обнаружения аномалий по волатильности
    threshold = 0.1#data['close'].std() * 2  # Порог аномалий (2 стандартных отклонения)
    anomalies = data[(data['close'].diff().abs() > threshold)]
    return anomalies
