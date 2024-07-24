#!/bin/bash
#
# Copy the common files (excluding `docker_name.sh`)
#   from the common central location (i.e., `docker_common`)
#   to a tutorial dir
#

set -e
#set -x

CURRENT_DIR=$(basename "$PWD")
# Check if the directory name contains "tutorial_"
if [[ "$CURRENT_DIR" != *"tutorial_"* ]]; then
    echo "Invalid current dir: $CURRENT_DIR"
    exit -1
fi;

#FILES=$(find . -name "docker_*.sh" -depth 1 | grep -v docker_name.sh)
FILES="docker_bash.sh docker_build.sh docker_clean.sh docker_cmd.sh docker_exec.sh docker_jupyter.sh docker_push.sh"
# Files in the Docker container.
FILES="$FILES bashrc etc_sudoers install_jupyter_extensions.sh run_jupyter.sh version.sh"

for FILE in $FILES
do
    echo "Copying '$FILE' to docker_common"
    cp -f $FILE ../../docker_common/$FILE
done;
