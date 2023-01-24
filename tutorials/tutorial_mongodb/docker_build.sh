#!/usr/bin -e

GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/utils.sh

IMAGE_NAME=umd_data605_mongodb
REPO_NAME=gpsaggese

# Build container.
#export DOCKER_BUILDKIT=1
export DOCKER_BUILDKIT=0
build_container_image
