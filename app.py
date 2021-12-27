from os import rename
from textwrap import indent
import streamlit as st 
import helper
st.set_page_config(
page_title="Copyright © 2021 Hasnain",
page_icon="🎢",
layout="wide",
initial_sidebar_state="expanded")
from datetime import date, datetime

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

#START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

col1, col2, col3, col4 = st.columns(4)
with col1 :
    selected_stock = st.text_input('Enter Stock Ticker', 'AAPL')
with col2 :
    start_date = st.text_input('Enter Start Date e.g, 1996-01-01 ', '1996-01-01')
with col3:
    end_date = st.text_input(f'Enter End Date e.g {TODAY} ', TODAY)
with col4:
    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365

lets_go = st.button('Make Prediction')

if lets_go:
    data_load_state = st.text('Loading data...')
    data = helper.load_data(selected_stock, start_date, end_date)
    data_load_state.text('Data Loaded Successfully!')

    st.subheader(f'Raw data from {start_date} ~ {end_date}')
    st.text('First Five Rows')
    st.write(data.head())
    st.text('Last Five Rows')
    st.write(data.tail())

    st.subheader(f'Data Summary from {start_date} ~ {end_date}')
    st.write(data.describe())

    helper.ma_comparison(data)
    
    with st.spinner(f'Generating the forecaset for {period} days, please stay with me...'):
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        df_forecast = forecast[['ds', 'yhat']].tail(period)
        col1, col2 = st.columns(2)
        with col1: 
            helper.plot_raw_data(data)
        with col2:
            st. header('Initial 5 days of complete Forecast')
            st.table(df_forecast.head(5))
            df_to_download = df_forecast.rename(columns={'ds':'Date', 'yhat':'Closing Price'}).to_csv(index=False).encode('utf-8')
            st.download_button(
            "Download complete forecasting",
            df_to_download,
            f"stock-forecast-downloaded-{datetime.now().strftime('%H:%M:%S')}.csv",
            "text/csv",
            key='download-csv'
            )

    st.header(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.header("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
