FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y \
    sudo curl systemctl gnupg git

# Install Python.
RUN apt install -y python3

# Install Postgres toolchain.
RUN apt-get -y update
RUN apt install -y \
    python3-pip python3-dev

RUN apt install -y \
    postgresql postgresql-contrib \
    libpq-dev

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

RUN mkdir /install
# Install Jupyter extensions.
ADD install_jupyter_extensions.sh /install
#
ADD etc_sudoers /install/
COPY etc_sudoers /etc/sudoers
COPY .bashrc /var/lib/postgresql/.bashrc

# Set the config for PostgreSQL server.
ADD project_postgres/postgresql.conf project_postgres/pg_hba.conf /install
RUN cp /install/postgresql.conf /etc/postgresql/14/main
RUN cp /install/pg_hba.conf /etc/postgresql/14/main

USER postgres
RUN /install/install_jupyter_extensions.sh

# Postgres.
EXPOSE 5432
# Jupyter.
EXPOSE 8888
