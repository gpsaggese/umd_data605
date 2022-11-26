#!/bin/bash -xe

IMAGE_NAME=umd_data605_spring2023_dask
CONTAINER_NAME=umd_data605_spring2023_dask
docker run --rm -ti --name $CONTAINER_NAME -p 8888:8888 -v $(pwd):/data $IMAGE_NAME
