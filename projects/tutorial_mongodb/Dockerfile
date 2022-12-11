FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y \
    sudo curl systemctl gnupg git

# Install Python.
RUN apt install -y python3

RUN apt install -y \
    jupyter-notebook \
    vim

# Install Python packages.
RUN pip3 install \
    jupyter \
    yapf \
    ipython \
    ipython-sql \
    psycopg2

RUN pip3 install \
    jupyter-contrib-core \
    jupyter-contrib-nbextensions

# Install MongoDB.
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add - && \
  echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
  apt update && \
  curl -O http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
  dpkg -i ./libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
  apt install -y mongodb-org mongodb-org-server mongodb-org-shell

RUN pip3 install pymongo \
    ipython-mongo

RUN mkdir /install
# Install Jupyter extensions.
ADD install_jupyter_extensions.sh /install
#
ADD etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY .bashrc /var/lib/postgresql/.bashrc

RUN /install/install_jupyter_extensions.sh

# Jupyter.
EXPOSE 8888
