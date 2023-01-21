#!/usr/bin/env bash -xe

IMAGE_NAME=umd_data605_mongodb
REPO_NAME=gpsaggese
FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME

# Prepare build area.
#tar -czh . | docker build $OPTS -t $IMAGE_NAME -
DIR="tmp.build"
if [[ -d $DIR ]]; then
    rm -rf $DIR
fi;
cp -Lr . $DIR

# Build container.
#export DOCKER_BUILDKIT=1
export DOCKER_BUILDKIT=0
OPTS="--progress plain $@"
(cd $DIR; docker build $OPTS -t $FULL_IMAGE_NAME . 2>&1 | tee ../docker_build.log; exit ${PIPESTATUS[0]})

# Report build version.
docker run --rm -ti -v $(pwd):/data $IMAGE_NAME bash -c "/data/version.sh 2>&1 | tee /data/docker_build.version.log"

# Push to repo.
docker image tag $IMAGE_NAME $FULL_IMAGE_NAME
docker image ls $REPO_NAME/$IMAGE_NAME
