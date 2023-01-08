#!/bin/bash -xe
source /Users/saggese/src/umd_data605/projects/tutorial_git/restart.sh

git status -s

touch work_main.py

git status -s

git add work_main.py

git status -s

git log --graph --oneline -3

git commit -am "Add work_main.py"

git log --graph --oneline -3
