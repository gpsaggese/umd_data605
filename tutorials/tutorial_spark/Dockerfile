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
    yapf \
    ipython \
    jupyter-contrib-core \
    jupyter-contrib-nbextensions

##COPY bashrc /var/lib/postgresql/.bashrc
RUN mkdir /install
ADD install_jupyter_extensions.sh /install
RUN /install/install_jupyter_extensions.sh

# Install java.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    java --version
ENV JAVA_HOME=/usr

# Install Spark.
RUN curl https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz --output spark.tgz && \
  tar zxvf spark.tgz && \
  rm -rf spark.tgz && \
  /spark-3.3.1-bin-hadoop3/bin/pyspark --version
# root@8da308e57d5e:/# $SPARKHOME/bin/pyspark --version
# Welcome to
#       ____              __
#      / __/__  ___ _____/ /__
#     _\ \/ _ \/ _ `/ __/  '_/
#    /___/ .__/\_,_/_/ /_/\_\   version 3.3.1
#       /_/
# 
# Using Scala version 2.12.15, OpenJDK 64-Bit Server VM, 11.0.17
# Branch HEAD
# Compiled by user yumwang on 2022-10-15T09:47:01Z
# Revision fbbcf9434ac070dd4ced4fb9efe32899c6db12a9
# Url https://github.com/apache/spark
# Type --help for more information.
ENV SPARKHOME=/spark-3.3.1-bin-hadoop3
ENV PYSPARK_PYTHON=/usr/bin/python3
ENV PYSPARK_DRIVER_PYTHON="jupyter"
ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888"
RUN $SPARKHOME/bin/pyspark --version

EXPOSE 8888
EXPOSE 4040
