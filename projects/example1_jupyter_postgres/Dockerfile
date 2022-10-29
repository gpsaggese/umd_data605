FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y python3-pip python3-dev postgresql postgresql-contrib libpq-dev jupyter-notebook vim
RUN pip3 install jupyter ipython-sql psycopg2

ADD smallRelationsInsertFile.sql largeRelationsInsertFile.sql DDL.sql postgresql.conf pg_hba.conf /datatemp/

# Set the config for PostgreSQL server.
RUN cp /datatemp/postgresql.conf /etc/postgresql/14/main
RUN cp /datatemp/pg_hba.conf /etc/postgresql/14/main

EXPOSE 8888
EXPOSE 5432

USER postgres

# ENTRYPOINT /etc/init.d/postgresql start && \
#     createdb university && \
#     psql --command "\i /datatemp/DDL.sql;" university && \
#     psql --command "\i /datatemp/smallRelationsInsertFile.sql;" university && \
#     psql --command "\i /datatemp/smallRelationsInsertFile.sql;" university
