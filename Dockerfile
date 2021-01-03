FROM python:3.9

WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./api/utils/setup/download_sentence_transformer.py /app/api/utils/setup/download_sentence_transformer.py
RUN python3 ./api/utils/setup/download_sentence_transformer.py

COPY . /app
