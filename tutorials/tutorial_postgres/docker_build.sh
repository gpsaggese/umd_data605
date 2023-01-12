#!/bin/bash -xe

IMAGE_NAME=umd_data605_postgres
export DOCKER_BUILDKIT=1
OPTS="--progress plain $@"
#tar -czh . | docker build $OPTS -t $IMAGE_NAME -
DIR="tmp.build"
if [[ -d $DIR ]]; then
    rm -rf $DIR
fi;
cp -Lr . $DIR
(cd $DIR; docker build $OPTS -t $IMAGE_NAME .)
