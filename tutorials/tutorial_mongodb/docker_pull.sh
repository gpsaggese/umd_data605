#!/usr/bin/env bash -e

GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/utils.sh

REPO_NAME=gpsaggese
IMAGE_NAME=umd_data605_mongodb

pull_container_image
