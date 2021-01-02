FROM python:3.9 AS base

WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

FROM base as dev
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./api/utils/setup/download_sentence_transformer.py /app/api/utils/setup/download_sentence_transformer.py
RUN python3 ./api/utils/setup/download_sentence_transformer.py

# The code gets volume mounted anyway in the model-dev container
# So, this step is part of the test-deploy stage
FROM dev as test-deploy
COPY . /app
