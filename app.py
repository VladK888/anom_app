import streamlit as st
import pandas as pd
from scripts.preprocessing import preprocess_data


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

