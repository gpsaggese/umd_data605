#!/bin/bash -xe

IMAGE_NAME=umd_data605_spring2023_pandas
CONTAINER_ID=$(docker container ls | grep $IMAGE_NAME | awk '{print $1}')
docker exec -it $CONTAINER_ID bash
