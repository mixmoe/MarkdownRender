FROM python:3.8-buster

COPY . /app

WORKDIR /app

ENV HOST=0.0.0.0 \
    PORT=8080 \
    FORWARDED_ALLOW_IPS="*"

RUN apt-get update && \
    apt-get install -y fonts-wqy-microhei ttf-wqy-microhei fonts-wqy-zenhei ttf-wqy-zenhei xfonts-75dpi xfonts-base && \
    curl -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb > /tmp/wkhtml.deb && \
    dpkg -i /tmp/wkhtml.deb && \
    fc-cache -f -v

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install -vvv

CMD cd /app && \
    uvicorn app:app --host $HOST --port $PORT