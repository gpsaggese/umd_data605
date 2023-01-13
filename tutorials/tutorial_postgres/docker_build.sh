#!/bin/bash -xe

IMAGE_NAME=umd_data605_postgres
REPO_NAME=gpsaggese
export DOCKER_BUILDKIT=1
OPTS="--progress plain $@"
#tar -czh . | docker build $OPTS -t $IMAGE_NAME -
DIR="tmp.build"
if [[ -d $DIR ]]; then
    rm -rf $DIR
fi;
cp -Lr . $DIR
(cd $DIR; docker build $OPTS -t $IMAGE_NAME .)
docker image tag umd_data605_postgres docker.io/$REPO_NAME/$IMAGE_NAME
docker image ls $REPO_NAME/$IMAGE_NAME
