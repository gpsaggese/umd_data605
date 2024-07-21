#!/bin/bash

run() {
  echo "$1"
  eval "$1"
}

BRANCH_NAME=$(git symbolic-ref --short HEAD)
echo $BRANCH_NAME

#run "git difftool $(git merge-base main $BRANCH_NAME)..$BRANCH_NAME"
run "git difftool $(git merge-base main $BRANCH_NAME).."
