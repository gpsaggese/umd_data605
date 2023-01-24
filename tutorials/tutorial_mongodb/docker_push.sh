#!/bin/bash -e

GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/utils.sh

IMAGE_NAME=umd_data605_mongodb
REPO_NAME=gpsaggese

push_container_image
