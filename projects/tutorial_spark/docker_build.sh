#!/bin/bash -xe

IMAGE_NAME=umd_data605_spring2023_spark
export DOCKER_BUILDKIT=1
OPTS="--progress plain"
docker build $OPTS -t $IMAGE_NAME .
