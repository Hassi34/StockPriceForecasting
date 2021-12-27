FROM python:3.7.12
COPY . /app
WORKDIR /app
RUN conda env create --file environment.yml
ENTRYPOINT [ "streamlit run" ]
CMD [ "app.py" ]