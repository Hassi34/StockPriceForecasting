import streamlit as st 
import yfinance as yf
from plotly import graph_objs as go
import matplotlib.pyplot as plt

@st.cache(suppress_st_warning=True)
def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start_date, end_date)
    st.text('load_data executed')
    data.reset_index(inplace=True)
    return data

def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series Data with Rangeslider', xaxis_rangeslider_visible=True)
    st.write(fig)

def ma_comparison(df):
    with st.spinner('Generating The Moving Average Comparison for you...'):
        st.subheader('Closing Price Vs Time Chart with 20MA, 100MA & 200MA')
        ma20 = df.Close.rolling(20).mean()
        ma100 = df.Close.rolling(100).mean()
        ma200 = df.Close.rolling(200).mean()
        fig = plt.figure(figsize=(12,6))
        plt.plot(df.Close, 'b', label = 'Daily Stock Trend')
        plt.plot(ma20, 'm', label='20 Days MA')
        plt.plot(ma100, 'r', label = '100 Days MA')
        plt.plot(ma200, 'g', label = '200 Days MA')
        plt.legend()
        st.pyplot(fig)
        st.success('Moving Average Comparision Generated!')
def candlestick(data, selected_stock):
        with st.spinner('Creating the candlestick chart...'):
            fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                name=selected_stock)])

            fig.update_xaxes(type='category')
            fig.update_layout(height=700)

            st.write(fig)