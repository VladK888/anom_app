import streamlit as st

st.title("FAQ")

st.subheader("Disclaimer")
st.write("The Temporal Corridors application provides only statistical information and data for the analysis of market assets. The company assumes no responsibility for any financial losses, damages, or other consequences resulting from the use of this application. The data presented and historical performance are not guarantees of future results and should not be construed as investment advice. Users make their own decisions related to trading or investing and bear full responsibility for their actions. Before making any financial transactions, it is strongly recommended to consult a professional financial advisor.")

st.subheader("Time Used for Analysis")
st.write("All statistical information and data presented in the Temporal Corridors application are based on the time corresponding to Universal Coordinated Time (UTC+3). The time indicated in the application may differ from the local time of users. Users are responsible for correctly understanding the time and its impact on their trading decisions. The application assumes no responsibility for users' decisions; all actions are made at the client's discretion.")

st.subheader("Price Change Analysis")
st.write("""
    **Change and Range Analysis**:
    - The code calculates how the prices of assets change relative to two key moving averages (SMA): **SMA 50** and **SMA 200**.
    - For each period (group of data), the application computes:
        - Absolute change (the difference between the starting and ending price).
        - Percentage change (how much the price changed compared to the starting price).
        - Absolute range (the difference between the maximum and minimum price).
        - Percentage range (how much the range changed relative to the starting price).

    **Comparison with Averages**:
    - The application counts the percentage of instances (periods) that exceed the average values of these changes and ranges. This helps determine how often an asset exhibits strong movements compared to its average behavior.

    **Visualization**:
    - **Price and SMA Chart**: Displays how the asset's price changes over time, along with the moving averages (SMA). This allows users to visually assess whether the price is above or below the SMA and when this occurs.
    - **Range Histogram**: Shows the distribution of price ranges over a specific period, helping to understand how volatile the prices have been.
    - **Correlation**: The application displays the correlation between closing price and SMA, which can help in understanding how the price relates to its moving average.
    - **Time Spent Above/Below SMA**: Illustrates how long the asset stays above or below the SMA, which is important for trend analysis.
    - **Boxplot**: Compares changes and ranges for cases above and below the SMA, providing insights into the asset's volatility.

    **Percentage of Achieved Averages**:
    - The application shows the percentage of instances where the asset demonstrates significant changes and ranges above or below its average values, which can aid in trading decisions.

    **Overview**:
    - The application provides only statistical information, and users should exercise caution when making financial decisions.
    """)

# Заголовок приложения
st.subheader("Seasonality Analysis")
st.write("""
    **Overview**
        Our application helps you analyze different financial instruments (like currencies, commodities, and indices) to identify seasonal trends and patterns. This is crucial for making informed trading decisions. We do this through various analyses, visualizations, and insights derived from historical data.

    **Key Components of the Analysis**

    - **Seasonal Analysis**:
       - We examine how the price movements of a selected financial instrument change over different months of the year. This can help identify whether certain months tend to yield higher profits or losses, allowing you to make better trading decisions.

    - **Data Visualization**:
       - The application creates clear visualizations, including bar charts and heatmaps, to illustrate important metrics. These charts show trends such as:
         - **Median Price Differences**: The typical change in price for each month.
         - **SMA (Simple Moving Average) Differences**: This helps in understanding the average price trends over time.
         - **Maximum Movement**: How much the price fluctuates during the month.

    - **Monthly and Weekly Patterns**:
       - By analyzing data over months and breaking it down by days of the week and hours, we can observe specific patterns. For example, you might notice that prices tend to rise more frequently on Mondays or during certain hours of the day.

    - **Heatmaps**:
       - Heatmaps provide a visual representation of the data, making it easy to identify high and low values at a glance. They help you see:
         - **Range of Prices**: How the price range varies by day and hour.
         - **Up/Down Movement**: How often the price goes up or down at different times of the week.

    **Trading Strategy**
    Based on this analysis, you can develop a strategy that aligns with the seasonal patterns identified:

    - **Timing Your Trades**: 
       - Use the information about which months are typically profitable to time your trades better. For example, if historical data shows that a particular currency usually rises in April, you might consider buying that currency in March.

    - **Understanding Daily Patterns**:
       - If the analysis indicates that prices are more volatile on certain days or hours, you can adjust your trading schedule to take advantage of these fluctuations. For example, if prices tend to drop on Wednesdays, you may decide to sell on that day.

    - **Adjusting for Volatility**:
       - Knowing the maximum and minimum movements can help you set appropriate stop-loss and take-profit levels, protecting your investments while maximizing potential gains.

    **Conclusion**
    In summary, our application provides you with a comprehensive analysis of seasonal trends in financial markets. By understanding these patterns, you can make more informed trading decisions, ultimately enhancing your chances of success. The combination of clear visualizations and strategic insights makes it easier for you to navigate the complexities of trading.
    """)
# Заголовок приложения
st.subheader("Price Anomaly Analysis")
st.write("""
    **Overview**
    The Temporal Corridors application focuses on detecting anomalies in financial market data by analyzing historical price movements and significant news events. Understanding anomalies can help traders make informed decisions based on how specific events influence asset prices.

    **Key Components of the Analysis**

    - **Anomaly Detection**:
       - This analysis identifies significant deviations in asset prices that correspond to major news events. By examining how prices react to these events, traders can discern patterns that may indicate future price movements.

    - **Event Integration**:
       - The application merges price data with relevant news events to visualize the impact of these events on asset prices. This allows traders to understand the context behind price movements.

    - **Visualization**:
       - The application uses interactive Plotly graphs to display price movements along with markers indicating significant news events. These markers represent instances where an event occurred, providing a clear visual reference for price changes.

    - **Event Information Table**:
       - A summary table shows the events that have influenced price movements, giving traders quick access to relevant information that can aid their decision-making processes.
    """)

st.subheader("Investment Analysis")
st.write("""
    - **What is the purpose of this investment simulation tool?**: 
        - This tool allows users to simulate and analyze different trading strategies, including Moving Average, Mean Reversion, and Seasonality Analysis. Users can upload their historical market data and visualize the performance of these strategies.,
        
    - **How does the Moving Average strategy work?**: 
        - The Moving Average strategy calculates two simple moving averages (SMA) over defined periods. It generates buy signals when the short-term SMA crosses above the long-term SMA and sell signals when it crosses below. The tool simulates trades based on these signals and visualizes the results.",
        
    - **What is Mean Reversion and how is it used here?**: 
        - Mean Reversion is based on the idea that asset prices tend to revert to their historical average over time. This strategy calculates the Z-score, which indicates how far the current price is from its moving average. Users can set a Z-score threshold to generate buy/sell signals based on price movements relative to this average.",
        
    - **What kind of data can I upload for analysis?**: 
        - Users can upload historical price data in CSV format, which should contain a 'date' column and a 'close' column. The tool will use the 'close' prices for analysis.",
        
    - **How are results visualized?**: 
        - The tool provides various visualizations, including price plots with buy/sell signals, cumulative returns, and bar plots for average hourly and weekday returns, making it easier to interpret the performance of each strategy.",
        
    - **Can I adjust the parameters of the strategies?**: 
        - Yes! The app allows you to dynamically adjust parameters such as the SMA windows for the Moving Average strategy and the Z-score threshold for the Mean Reversion strategy through sliders and input fields in the sidebar.",
        
    - **Is there an option to export the results?**: 
        - While the current version does not include a direct export feature, users can take screenshots of the visualizations for their records.""")

st.subheader("Main menu (app)")

st.write("- **What is the Close Price?**")
st.write("The Close Price is the last trading price of the asset at the end of the trading day. It is used to evaluate market performance and is a key metric for traders.")

st.write("- **What does the 200-Day Difference (High - Low) represent?**")
st.write("This metric measures the difference between the highest and lowest prices of the asset over the last 200 days. It helps identify the asset's price volatility and trading range.")

st.write("- **What is the Z-Score of Close Price?**")
st.write("The Z-Score is a statistical measure that indicates how many standard deviations a data point is from the mean. In this context, it helps identify whether the current price is overbought or oversold relative to historical prices.")

st.write("- **How can I use this information for trading?**")
st.write("By analyzing the Close Price along with the 200-Day Difference and the Z-Score, traders can make informed decisions about potential entry or exit points in the market. A high Z-Score may indicate overbought conditions, while a low Z-Score may suggest oversold conditions.")


