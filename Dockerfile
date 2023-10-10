FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev postgresql-client libffi-dev

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . .
