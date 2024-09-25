import streamlit as st
import pandas as pd
from scripts.preprocessing import preprocess_data
from scripts.visualization import plot_price_chart,load_data



# Load data
file_path = 'data/gold_d.csv'
data = pd.read_csv(file_path)

# Preprocess data
data = preprocess_data(data)

st.title("The Temporal Corridors")

plot_price_chart(data)



