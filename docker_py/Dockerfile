# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements_flask.txt requirements_flask.txt
RUN pip install -r requirements_flask.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

