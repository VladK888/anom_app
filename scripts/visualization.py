import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st
import pandas as pd


def load_data(symbol):
    # Function to load data from CSV
    file_path = f'data/{symbol}_data.csv'
    try:
        df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
        return df
    except FileNotFoundError:
        st.error(f"Data file for {symbol} not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return None


def plot_price_chart():
    # List of symbols
    symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']

    # Application title
    st.title("The Temporal Corridors")

    # Symbol selection
    selected_symbol = st.selectbox("Choose symbol", symbols, key="analyzer_symbol")

    # Load data for the selected symbol
    data = load_data(selected_symbol)
    if data is None:
        return  # Stop execution if data is not loaded

    # Check for required columns
    required_columns = ['close', 'range', 'Z-Score']
    for column in required_columns:
        if column not in data.columns:
            st.error(f"Column '{column}' is missing from the data.")
            return  # Stop execution if a required column is missing

    # Create a figure with subplots
    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True,
                           subplot_titles=('Close Price', '200-Day Difference (High - Low)', 'Z-Score of Close Price'))

    # Plot Close Price
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Close Price', line=dict(color='blue')), row=1, col=1)

    # Plot 200-Day Difference (assuming 'range' is the correct column)
    fig.add_trace(go.Scatter(x=data.index, y=data['range'], mode='lines', name='200-Day Difference (High - Low)', line=dict(color='red')), row=2, col=1)

    # Plot Z-Score
    fig.add_trace(go.Scatter(x=data.index, y=data['Z-Score'], mode='lines', name='Z-Score of Close Price', line=dict(color='purple')), row=3, col=1)

    # Update layout
    fig.update_layout(height=1000, width=800, title_text="Combined Financial Metrics", showlegend=True)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Difference", row=2, col=1)
    fig.update_yaxes(title_text="Z-Score", row=3, col=1)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    # Disclaimer
    st.write("Disclaimer")
    st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")


