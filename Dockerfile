FROM python:latest as builder

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt-get update; apt-get upgrade -y

LABEL fly_launch_runtime="python"

# Install poetry separated from system interpreter
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry config experimental.new-installer false

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN poetry install --no-dev --no-root

CMD [ "poetry", "run", "python", "main.py" ]