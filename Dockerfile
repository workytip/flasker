# simple docker file for flask app for DEPI DevOps Training
FROM python:3.12 

WORKDIR /app/flasker

USER root 

RUN pip install Flask Werkzeug wheel Jinja2 click
COPY flasker .
COPY pyproject.toml ..

WORKDIR /app 

RUN flask --app flasker init-db


ENTRYPOINT [ "flask",  "--app", "flasker", "run",  "--host=0.0.0.0" ]

EXPOSE 5000