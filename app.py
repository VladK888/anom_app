import streamlit as st
import pandas as pd
from scripts.preprocessing import preprocess_data, calculate_duration_and_changes
from scripts.analyzer import analyzer
from scripts.seasonality import seasonality
from scripts.investment_sim import investment_simulation
from scripts.anomaly_detection import detect_anomalies
from visualization import plot_price_chart

# Password protection
def password_protection():
    st.title("Protected Application")
    password = st.text_input("Enter password", type="password")
    if password != "your_password":  # Replace "your_password" with your actual password
        st.error("Invalid password")
        st.stop()  # Stop the application if the password is incorrect

password_protection()  # Call the password protection function

# Load data
file_path = 'data/gold_d.csv'
data = pd.read_csv(file_path)

# Preprocess data
data = preprocess_data(data)

# Navigation for tabs
tab = st.sidebar.selectbox("Select a tab", ("Investment Simulation", "Analysis", "Seasonality","Anomalies"))

if tab == "Investment Simulation":
    # Select symbol
    symbols = data['symbol'].unique()
    selected_symbol = st.selectbox("Choose symbol", symbols, key="symbol_selectbox")

    # Filter data by selected symbol
    filtered_data = data[data['symbol'] == selected_symbol]

    # Date range selection
    start_date = st.date_input("Select start date", value=filtered_data.index.min())
    end_date = st.date_input("Select end date", value=filtered_data.index.max())

    # Filter data by selected date range
    filtered_data = filtered_data.loc[start_date:end_date]

    # Plotting charts
    st.title("Time Corridors: Analysis of Financial Anomalies")
    plot_price_chart(filtered_data)

    # Investment simulation
    st.header("Investment Simulator")
    investment_simulation(filtered_data)

elif tab == "Analysis":
    # Select symbol
    analyzer()

elif tab == "Seasonality":
    # Call seasonality function (assumed to have its own logic)
    seasonality()

elif tab == "Anomalies":
    # Call seasonality function (assumed to have its own logic)
    detect_anomalies(symbol)
