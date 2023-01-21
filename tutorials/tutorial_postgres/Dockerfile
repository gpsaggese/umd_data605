FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

# Install system utilities.
RUN apt install -y --no-install-recommends \
    sudo \
    curl \
    systemctl \
    gnupg \
    git \
    vim

# Install Python.
RUN apt install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev

# Install Python packages.
RUN pip3 install \
    jupyter \
    yapf \
    ipython \
    ipython-sql \
    psycopg2-binary \
    jupyter-contrib-core \
    jupyter-contrib-nbextensions \
    yapf

RUN mkdir /install

# Install Postgres.
RUN apt install -y \
    postgresql \
    postgresql-contrib \
    libpq-dev

ADD etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY bashrc /var/lib/postgresql/.bashrc

# Set the config for PostgreSQL server.
ADD postgresql.conf pg_hba.conf /install/
RUN cp /install/postgresql.conf /etc/postgresql/14/main
RUN cp /install/pg_hba.conf /etc/postgresql/14/main

USER postgres

# Install Jupyter extensions.
ADD install_jupyter_extensions.sh /install/
RUN /install/install_jupyter_extensions.sh

# Report package versions.
ADD version.sh /install/
RUN /install/version.sh 2>&1 | tee version.log

# Postgres.
EXPOSE 5432
# Jupyter.
EXPOSE 8888
