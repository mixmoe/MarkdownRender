FROM python:3.8-buster

COPY . /app

WORKDIR /app

ENV HOST=0.0.0.0 PORT=8080

RUN apt-get update && \
    apt-get install -y ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy wkhtmltopdf

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install -vvv

CMD cd /app && \
    uvicorn app:app --host $HOST --port $PORT