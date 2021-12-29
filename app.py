from numpy.core.numeric import ones_like
import streamlit as st 
import stockForecasting
import customForecating
import helper
st.set_page_config(
page_title="Copyright © 2021 Hasnain",
page_icon="🎢",
layout="wide")
stocks = stockForecasting.StockForecasting()
st.sidebar.title('Real-time Forecating App')
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROf1dea9H0pSgxQPa_u8vZraz3EtMkeS3K9rjwmlDTJj_WV0WxA_82oa5w-3r7vty8SH0&usqp=CAU')
option = st.sidebar.radio(
     'What kind of analysis you want to perform ?',
     ('Stock Price Prediction', 'Custom Prediction'))
st.sidebar.write('Current selection is ', f'"{option}"')

if option == 'Stock Price Prediction' :
    try: 
        selected_stock, start_date, end_date, period = stocks.stock_forecast()
        st.sidebar.button('Make Prediction', on_click=stocks.prediction, args=[selected_stock, start_date, end_date, period])
    except:
        st.subheader('Something Went Wrong with the Selection, please make the selection again')
if option == 'Custom Prediction':
    customForecating.custom_predictions()


st.sidebar.header('Get the Code')
github_link = '[GitHub](https://github.com/Hassi34/StockPriceForecasting.git)'
st.sidebar.markdown(github_link, unsafe_allow_html=True)
portfolio_link = '[My Portfolio](https://hasnainmehmood.pythonanywhere.com/)'
st.sidebar.markdown(portfolio_link, unsafe_allow_html=True)