import streamlit as st
import pandas as pd
from scripts.preprocessing import preprocess_data
from scripts.preprocessing import visualization



# Load data
file_path = 'data/gold_d.csv'
data = pd.read_csv(file_path)

# Preprocess data
data = preprocess_data(data)

st.title("The Temporal Corridors")

plot_price_chart(data)

st.write("Disclaimer ")
st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")



