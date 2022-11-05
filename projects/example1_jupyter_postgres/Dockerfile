FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y \
    sudo curl systemctl gnupg

# Install python.
RUN apt install -y python3

# Install SQL toolchain.
RUN apt install -y \
    python3-pip python3-dev \
    postgresql postgresql-contrib \
    libpq-dev \
    jupyter-notebook \
    vim

# Install Python packages.
RUN pip3 install \
    jupyter \
    ipython \
    ipython-sql \
    psycopg2

RUN pip3 install \
    jupyter-contrib-core \
    jupyter-contrib-nbextensions

RUN apt install -y \
    git

ADD etc_sudoers /datatemp/
COPY etc_sudoers /etc/sudoers
COPY .bashrc /var/lib/postgresql/.bashrc

# Set the config for PostgreSQL server.
ADD postgresql.conf pg_hba.conf /datatemp/
RUN cp /datatemp/postgresql.conf /etc/postgresql/14/main
RUN cp /datatemp/pg_hba.conf /etc/postgresql/14/main

# Add University DB.
ADD smallRelationsInsertFile.sql largeRelationsInsertFile.sql DDL.sql /datatemp/

EXPOSE 8888
EXPOSE 5432

USER postgres
