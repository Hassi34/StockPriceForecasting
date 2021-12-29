import pandas as pd 
from fbprophet import Prophet
import streamlit as st
import helper
from datetime import datetime
from fbprophet.plot import plot_plotly

def custom_predictions():
    uploaded_file = st.sidebar.file_uploader('Choose a file having ".csv" extention')
    period = int(st.sidebar.number_input('Enter the number of days to be predicted'))
    lets_go = st.sidebar.button("Let's Go!")
    if lets_go:
        try:
            if uploaded_file is not None:
                # To read file as bytes:
                #data = uploaded_file.getvalue().decode('utf-8')
                df = pd.read_csv(uploaded_file)
                success = helper.validate_file(df)
                if success:
                    with st.spinner(f'Generating the Forecast for {period} days in future, please stay with me ☺'):
                        df = helper.custom_predictions_helper(df)
                        m = Prophet()
                        m.fit(df.rename(columns={'Date':'ds', 'y':'y'}))
                        future = m.make_future_dataframe(periods=period)
                        forecast = m.predict(future)
                        df_forecast = forecast[['ds', 'yhat']].rename(columns={'ds':'Date','yhat':'Forecast'}).tail(period)
                        #df_forecast['Date'] = pd.to_datetime(df_forecast['Date']).apply(lambda x : x.strftime("%Y-%m-%d"))

                        st.subheader('First 5 days of complete Forecast')
                        st.dataframe(df_forecast.head(5).reset_index(drop=True))
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

                else :
                    st.error("Could not run all test successfully, Please download the corrent format to complete the task")
                    df_required = pd.read_csv('https://raw.githubusercontent.com/Hassi34/Datasets/main/RequiredFormat.csv')
                    df_required = df_required.to_csv(index=False).encode('utf-8')
                    st.download_button(
                    '📥 Download Correct Format',
                    df_required,
                    "RequiredFormat.csv",
                    "text/csv",
                    key='download-csv'
                    )

        except:
            st.error("Could not run all test successfully, Please download the corrent format to complete the task")
            df_required = pd.read_csv('https://raw.githubusercontent.com/Hassi34/Datasets/main/RequiredFormat.csv')
            df_required = df_required.to_csv(index=False).encode('utf-8')
            st.download_button(
            '📥 Download Correct Format',
            df_required,
            "RequiredFormat.csv",
            "text/csv",
            key='download-csv'
            )