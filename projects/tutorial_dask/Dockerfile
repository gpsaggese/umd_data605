FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y \
    sudo curl systemctl gnupg git

# Install Python.
RUN apt-get update && apt install \
    -y \
    --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    jupyter-notebook \
    vim

# Install Python packages.
RUN pip3 install \
    jupyter \
    dask \
    pandas \
    matplotlib \
    yapf \
    ipython \
    jupyter-contrib-core \
    jupyter-contrib-nbextensions

# Install graphviz.
RUN apt install -y graphviz
RUN pip3 install graphviz.

RUN mkdir /install
ADD install_jupyter_extensions.sh /install
RUN /install/install_jupyter_extensions.sh

EXPOSE 8888
