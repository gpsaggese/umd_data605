#!/usr/bin/env bash

IMAGE_NAME=umd_data605_spring2023_pandas
export DOCKER_BUILDKIT=0
OPTS="--progress plain"
docker build $OPTS -t $IMAGE_NAME . 2>&1 | tee docker_build.log
docker run --rm -ti -v $(pwd):/data $IMAGE_NAME bash -c "/data/version.sh 2>&1 | tee /data/docker_build.version.log"
