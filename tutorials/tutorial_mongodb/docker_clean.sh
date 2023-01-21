#!/bin/bash -x

IMAGE_NAME=umd_data605_postgres
docker image ls | grep $IMAGE_NAME
docker image ls | grep $IMAGE_NAME | awk '{print $1}' | xargs -n 1 -t docker image rm -f
docker image ls
