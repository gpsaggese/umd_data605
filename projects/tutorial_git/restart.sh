#!/bin/bash -xe
if [[ -d /tmp/umd_data605_tmp ]]; then
    rm -rf /tmp/umd_data605_tmp
fi;
git clone git@github.com:gpsaggese/umd_data605.git /tmp/umd_data605_tmp
cd /tmp/umd_data605_tmp

ls -1
