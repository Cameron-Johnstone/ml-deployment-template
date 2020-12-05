FROM python:3.9 AS base

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && \
    pip install -r requirements.txt

FROM base as test-deploy
COPY . /app

# For local development environment
# Make sure to set the variables in the .env file
# Installing jupyter may overwrite existing package versions, 
# so pip freeze and update your requirements.txt later
FROM base AS dev
RUN pip install jupyter