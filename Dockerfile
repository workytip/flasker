FROM python:3.9-slim

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app


COPY pyproject.toml /usr/src/app/

RUN pip install Flask Werkzeug wheel Jinja2 click

COPY . /usr/src/app

EXPOSE 5000


CMD bash -c "flask --app flasker init-db && flask --app flasker run --host=0.0.0.0"



