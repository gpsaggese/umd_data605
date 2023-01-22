#!/bin/bash -xe

GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/utils.sh

REPO_NAME=gpsaggese
IMAGE_NAME=umd_data605_mongodb

push_container_image
