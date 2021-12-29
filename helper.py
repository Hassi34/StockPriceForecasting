import streamlit as st
from traitlets.traitlets import Instance 
import yfinance as yf
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import requests
import pandas as pd 

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
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

def ma_comparison(df, target_col = "Close"):
    with st.spinner('Generating The Moving Average Comparison for you...'):
        st.subheader('Closing Price Vs Time Chart with 20MA, 100MA & 200MA')
        ma20 = df[target_col].rolling(20).mean()
        ma100 = df[target_col].rolling(100).mean()
        ma200 = df[target_col].rolling(200).mean()
        fig = plt.figure(figsize=(12,6))
        plt.plot(df[target_col], 'b', label = 'Daily Stock Trend')
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
            fig.update_layout(height=600, width = 1000)

            st.write(fig)

def stocktwits(selected_stock):
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{selected_stock}.json")
    data = r.json()
    if data['response']['status']==200:
        st.subheader(f"Still not sure ? Don't worry we got you! check out what poeple are saying about '{selected_stock}'")
        for message in data['messages']:
            st.image(message['user']['avatar_url'])
            st.write(message['user']['username'])
            st.write(message['created_at'])
            st.write(message['body'])
def tests(data):
    success = True
    if len(data.columns) == 2:
        st.success('Test Passed : There are 2 column in the data')
        columns = (data.columns).str.lower()
        if 'date' in columns:
            st.success('Test Passed : "Date" column is available in the data.')
        elif 'date' not in columns:
            st.error('Test Failed : There is no "Date" Column avilable.' )
            success = False
        if 'y' in columns:
            st.success('Test Passed : "y" column is available in the data')
        elif 'y' not in columns:
            st.error('Test Failed : There is no "y" Column avilable.')
            success = False
 
    elif len(data.columns) != 2:
        st.error(f'Number of columns should be 2 while {len(data.columns)} were given!')
        success = False
    return success
def validate_file(data):
    if isinstance(data, pd.DataFrame):
        success = tests(data)
        if success: 
            st.balloons()
            st.success('All test passed : Data has been validated successfully!')
    else : 
        data = pd.DataFrame(data)
        success = tests(data)
        if success: 
            st.balloons()
            st.success('Data has been validated successfully!')
    return success

def custom_predictions_helper(data):
        data.columns = ['ds', 'y']
        data = data.dropna()
        data['ds'] = pd.to_datetime(data.ds).apply( lambda x : x.strftime("%Y-%m-%d"))
        st.subheader(f'Raw data from {data.ds.min()} ~ {data.ds.max()}')
        st.text('First Five Rows')
        st.write(data.head())
        st.text('Last Five Rows')
        st.write(data.tail())

        st.subheader(f'Data Summary from {data.ds.min()} ~ {data.ds.max()}')
        st.write(data.describe())
        ma_comparison(data, target_col='y')
        return data

        
