FROM python:3.9 AS base

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && \
    pip install -r requirements.txt

# For production/staging deployment CI/CD pipeline
FROM base as test-deploy
COPY . /app

# For local development environment (make sure to set the variables in the .env file) (installing jupyter may overwrite existing packages)
FROM base AS dev
RUN pip install jupyter
