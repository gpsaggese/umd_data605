#!/bin/bash -xe
cd /tmp
if [[ -d /tmp/umd_data605_tmp ]]; then
    rm -rf /tmp/umd_data605_tmp
fi;
git clone git@github.com:gpsaggese/umd_data605.git /tmp/umd_data605_tmp
cd /tmp/umd_data605_tmp
git remote rm origin

ls 
git status
git log --graph --oneline -3
