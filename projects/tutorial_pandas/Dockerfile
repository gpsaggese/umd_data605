FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y \
    sudo \
    curl \
    systemctl \
    gnupg \
    git \
    vim

# Install Python.
RUN apt install -y \
    python3 \
    python3-pip python3-dev

RUN python3 --version
RUN pip3 --version

RUN python3 -m pip install --upgrade pip
    
# Install Python packages.
RUN pip3 install \
    jupyter-contrib-core \
    jupyter-contrib-nbextensions \
    matplotlib \
    numpy \
    pandas \
    seaborn \
    yapf

RUN mkdir /install
ADD install_jupyter_extensions.sh /install

# Install Jupyter extensions.
RUN /install/install_jupyter_extensions.sh

# Config.
ADD etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc

# 
ADD version.sh /install/
RUN /install/version.sh 2>&1 | tee version.log

# Jupyter.
EXPOSE 8888
