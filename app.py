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
    selected_stock = st.text_input('Enter Ticker Symbol e.g. "BTC-USD" for Bitcoin', 'AAPL')
    st.markdown('Not sure about the ticker symbol ? '+'[Search here!](https://finance.yahoo.com/)'
                                                , unsafe_allow_html=True)
with col2 :
    start_date = st.text_input('Enter Start Date e.g, 1996-01-01 ', '1996-01-01')
    st.write('System will use this data to train the model for forecasting')
with col3:
    end_date = st.text_input(f'Enter End Date e.g {TODAY} ', TODAY)
    st.write('Kindly follow the given specific date format')
with col4:
    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365
    st.write('Select the number of years price is required to be predicted for.')

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

    with st.spinner(f'Generating the Forecast for {period} days in future, please stay with me ☺'):
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        df_forecast = forecast[['ds', 'yhat']].rename(columns={'ds':'Date','yhat':'Closing Price'}).tail(period)
        col1, col2 = st.columns(2)
        with col1: 
            helper.candlestick(data, selected_stock)
        with col2:
            st. header('Initial 5 days of complete Forecast')
            st.write(df_forecast.head(5).reset_index(drop=True))
            df_to_download = df_forecast.to_csv(index=False).encode('utf-8')
            st.download_button(
            "Download complete Forecast",
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

    st.header('Get the Code')
    github_link = '[GitHub](https://github.com/Hassi34/StockPriceForecasting.git)'
    st.markdown(github_link, unsafe_allow_html=True)
    portfolio_link = '[My Portfolio](https://hasnainmehmood.pythonanywhere.com/)'
    st.markdown(portfolio_link, unsafe_allow_html=True)