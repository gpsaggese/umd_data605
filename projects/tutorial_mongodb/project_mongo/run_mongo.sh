#!/bin/bash -xe
sudo systemctl enable mongod

sudo /usr/bin/mongod --config /etc/mongod.conf 2>&1 | tee ~/mongo.log &
