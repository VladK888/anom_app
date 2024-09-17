import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st
from scripts.preprocessing import  calculate_adx
import pandas as pd
import numpy as np

def plot_price_chart(data):
    # Calculate ADX and add it to the data
    data = calculate_adx(data, window=66)

    # Create a figure with subplots
    fig = sp.make_subplots(rows=6, cols=1, shared_xaxes=True,
                           subplot_titles=('Close Price', '22-Day Volatility', 'Sharpe Ratio', '22-Day Difference (High - Low)', 'Z-Score of Close Price', 'ADX'))

    # Plot Close Price
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Close Price', line=dict(color='blue')), row=1, col=1)

    # Plot Volatility
    fig.add_trace(go.Scatter(x=data.index, y=data['Volatility'], mode='lines', name='22-Day Volatility', line=dict(color='orange')), row=2, col=1)

    # Plot Sharpe Ratio
    fig.add_trace(go.Scatter(x=data.index, y=data['Sharpe Ratio'], mode='lines', name='Sharpe Ratio', line=dict(color='green')), row=3, col=1)

    # Plot 22-Day Difference
    fig.add_trace(go.Scatter(x=data.index, y=data['22-Day Difference'], mode='lines', name='22-Day Difference (High - Low)', line=dict(color='red')), row=4, col=1)

    # Plot Z-Score
    fig.add_trace(go.Scatter(x=data.index, y=data['Z-Score'], mode='lines', name='Z-Score of Close Price', line=dict(color='purple')), row=5, col=1)

    # Plot ADX
    fig.add_trace(go.Scatter(x=data.index, y=data['ADX'], mode='lines', name='ADX', line=dict(color='brown')), row=6, col=1)

    # Update layout
    fig.update_layout(height=1000, width=800, title_text="Combined Financial Metrics", showlegend=True)
    fig.update_xaxes(title_text="Date", row=6, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volatility", row=2, col=1)
    fig.update_yaxes(title_text="Sharpe Ratio", row=3, col=1)
    fig.update_yaxes(title_text="Difference", row=4, col=1)
    fig.update_yaxes(title_text="Z-Score", row=5, col=1)
    fig.update_yaxes(title_text="ADX", row=6, col=1)

    # Display plotly chart in Streamlit
    st.plotly_chart(fig)




