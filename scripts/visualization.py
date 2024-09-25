import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st
import pandas as pd


def plot_price_chart():
    # List of symbols
    symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'NG', 'UKOUSD', 'NAS100', 'US30', 'Coffee', 'BTCUSD']

    def load_data(symbol):
        file_path = f'data/{symbol}_data.csv'
        df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
        return df

    # Application title
    st.title("The Temporal Corridors")

    # Symbol selection
    selected_symbol = st.selectbox("Choose symbol", symbols, key="analyzer_symbol")

    # Load data for the selected symbol
    data = load_data(selected_symbol)

    data['Moving_Average'] = data['close'].rolling(window=50).mean()
    data['Moving_Std'] = data['close'].rolling(window=50).std()
    data['Z-score'] = (data['close'] - data['Moving_Average']) / data['Moving_Std']
    data['diff_d'] = (data['high'] - data['low']).rolling(window=200).mean()

    # Create a figure with subplots
    fig = sp.make_subplots(rows=3, cols=1, shared_xaxes=True,
                           subplot_titles=('close', 'diff_d', 'Z-score'))

    # Plot Close Price
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Close Price', line=dict(color='blue')), row=1, col=1)

    # Plot 200-Day Difference (assuming range is the correct column)
    fig.add_trace(go.Scatter(x=data.index, y=data['diff_d'], mode='lines', name='200-Day Difference (High - Low)', line=dict(color='red')), row=2, col=1)

    # Plot Z_Score
    fig.add_trace(go.Scatter(x=data.index, y=data['Z-score'], mode='lines', name='Z-Score of Close Price', line=dict(color='purple')), row=3, col=1)

    # Update layout
    fig.update_layout(height=1000, width=800, title_text="Combined Financial Metrics", showlegend=True)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="close", row=1, col=1)
    fig.update_yaxes(title_text="diff_d", row=2, col=1)
    fig.update_yaxes(title_text="Z-Score", row=3, col=1)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    # Disclaimer
    st.write("Disclaimer")
    st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")


