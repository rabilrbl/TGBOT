FROM python:latest

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["bash", "-c"]

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m mahiner && echo "mahiner:mahiner" | chpasswd && adduser mahiner sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER mahiner

WORKDIR /home/mahiner

RUN sudo apt-get update && sudo apt-get upgrade -y

RUN pip3 install --upgrade pip

WORKDIR /home/mahiner/Projects

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
