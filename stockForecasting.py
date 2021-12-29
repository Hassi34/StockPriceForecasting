import streamlit as st 
import helper
from datetime import date, datetime
import pandas as pd
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
class StockForecasting:
    def __init__(self):
        pass 
    def stock_forecast(self):
        #st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROf1dea9H0pSgxQPa_u8vZraz3EtMkeS3K9rjwmlDTJj_WV0WxA_82oa5w-3r7vty8SH0&usqp=CAU', 
        #            use_column_width='always')
        TODAY = date.today().strftime("%Y-%m-%d")

        #st.sidebar.title('Stock Forecast App')
        selected_stock = st.sidebar.text_input('Enter Ticker Symbol e.g. "BTC-USD" for Bitcoin', 'AAPL')
        st.sidebar.markdown('Not sure about the ticker symbol ? '+'[Search here!](https://finance.yahoo.com/)'
                                                    , unsafe_allow_html=True)
        start_date = st.sidebar.text_input('Enter Start Date e.g. 1996-01-01 ', '1996-01-01')
        st.sidebar.write('System will use this data to train the model for forecasting')

        end_date = st.sidebar.text_input(f'Enter End Date e.g. {TODAY} ', TODAY)

        n_years = st.sidebar.slider('Years of prediction:', min_value = 0.5, max_value = 6.0,  step = 0.5)
        period = int(n_years * 365)
        
        return selected_stock, start_date, end_date, period

    def prediction(self, selected_stock, start_date, end_date, period):
        data_load_state = st.text('Loading data...')
        data = helper.load_data(selected_stock, start_date, end_date)
        data_load_state.text('Data Loaded Successfully!')
        data['Date'] = pd.to_datetime(data.Date).apply( lambda x : x.strftime("%Y-%m-%d"))

        st.subheader(f'Raw data from {start_date} ~ {end_date}')
        st.text('First Five Rows')
        st.write(data.head())
        st.text('Last Five Rows')
        st.write(data.tail())

        st.subheader(f'Data Summary from {start_date} ~ {end_date}')
        st.write(data.describe())

        helper.ma_comparison(data)
        st.subheader("Candlestick Chart")
        helper.candlestick(data, selected_stock)

        with st.spinner(f'Generating the Forecast for {period} days in future, please stay with me ☺'):
            df_train = data[['Date','Close']]
            df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)

            df_forecast = forecast[['ds', 'yhat']].rename(columns={'ds':'Date','yhat':'Closing Price'}).tail(period)
            df_forecast['Date'] = pd.to_datetime(df_forecast['Date']).apply(lambda x : x.strftime("%Y-%m-%d"))

            st.subheader('First 10 days of complete Forecast')
            st.dataframe(df_forecast.head(10).reset_index(drop=True))
            df_to_download = df_forecast.to_csv(index=False).encode('utf-8')
            st.download_button(
            "📥 Download complete Forecast",
            df_to_download,
            f"stock-forecast-downloaded-{datetime.now().strftime('%H:%M:%S')}.csv",
            "text/csv",
            key='download-csv'
            )

            st.header(f'Forecast plot for {period} days')
            fig1 = plot_plotly(m, forecast)
            st.plotly_chart(fig1)

            st.header("Forecast components")
            fig2 = m.plot_components(forecast)
            st.write(fig2)
        try:
            helper.stocktwits(selected_stock)
        except: 
            pass