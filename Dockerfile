FROM python:3.8-buster

COPY . /app

WORKDIR /app

ENV HOST=0.0.0.0 PORT=8080

RUN curl -L https://github.com/jarrekk/imgkit/raw/master/travis/init.sh | bash - && \
    apt-get install ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install -vvv

CMD cd /app && \
    uvicorn app:app --host $HOST --port $PORT