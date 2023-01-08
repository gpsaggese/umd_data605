#!/bin/bash -xe
if [[ -d /tmp/umd_data605_tmp ]]; then
    rm -rf /tmp/umd_data605_tmp
fi;
git clone git@github.com:gpsaggese/umd_data605.git /tmp/umd_data605_tmp
cd /tmp/umd_data605_tmp
ls -1

git status -s

touch work_main.py

git status -s

git add work_main.py

git status -s

git log --graph --oneline -3

git commit -am "Add work_main.py"

git log --graph --oneline -3
