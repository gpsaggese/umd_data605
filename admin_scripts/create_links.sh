#!/bin/bash

set -e
#set -x

FILES="docker_bash.sh docker_build.sh docker_clean.sh docker_cmd.sh docker_exec.sh docker_jupyter.sh docker_push.sh"
# Files in the Docker container.
FILES="$FILES bashrc etc_sudoers install_jupyter_extensions.sh run_jupyter.sh version.sh"

for FILE in $FILES
do
    echo "Creating link for '$FILE'"
    if [[ -f $FILE ]]; then
        rm -f $FILE
    fi;
    ln -s ../../docker_common/$FILE .
done;
