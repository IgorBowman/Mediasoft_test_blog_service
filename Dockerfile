FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /mediasofttestblog
COPY requirements.txt /mediasofttestblog/

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt \

COPY . /mediasofttestblog/
