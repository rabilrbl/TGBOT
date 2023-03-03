FROM python:latest as builder

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt-get update; apt-get upgrade -y

LABEL fly_launch_runtime="python"

# Install poetry separated from system interpreter
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add ~/.local/bin to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Poetry config: https://python-poetry.org/docs/configuration/
# As we are on docker, we don't need virtual environments
RUN poetry config virtualenvs.create false

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN poetry install --only main --no-root

CMD [ "poetry", "run", "tgbot" ]