#!/bin/bash -xe
restart.sh

git checkout -b iss53

git status -s

touch feature.py

git status -s

git add feature.py

git status -s

git log --graph --oneline -3

git commit -am "Add work_main.py"

git log --graph --oneline -3
