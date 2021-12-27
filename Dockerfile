FROM python:3.8.0 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "streamlit run" ]
CMD [ "app.py" ]