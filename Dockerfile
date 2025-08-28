FROM python:3.9-slim

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY pyproject.toml /usr/src/app/

RUN pip install Flask Werkzeug wheel Jinja2 click

COPY . /usr/src/app

# Set the FLASK_APP environment variable
ENV FLASK_APP=flasker.py

# Initialize database during build
RUN flask init-db

EXPOSE 5000

# Proper CMD format - single command
CMD ["flask", "run", "--host=0.0.0.0"]