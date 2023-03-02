FROM python:latest as builder

RUN apt-get update; apt-get upgrade -y

#######################################################################

LABEL fly_launch_runtime="python"

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]