FROM python:latest

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["bash", "-c"]

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m rabil && echo "rabil:rabil" | chpasswd && adduser rabil sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER rabil

WORKDIR /home/rabil

RUN sudo apt-get update && sudo apt-get upgrade -y

RUN sudo apt-get install curl docker -y

# Install and configure fish shell
RUN sudo apt-get install -y fish \
        && sudo chsh -s /usr/bin/fish rabil \
        && fish -c "curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher" \
        && fish -c "fisher install jethrokuan/z" \
        && fish -c "fisher install jethrokuan/fzf"

SHELL ["fish", "-c"]
