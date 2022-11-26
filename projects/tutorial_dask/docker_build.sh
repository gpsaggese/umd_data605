#!/bin/bash -xe

IMAGE_NAME=umd_data605_spring2023_dask
docker build -t $IMAGE_NAME .
