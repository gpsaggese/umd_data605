#!/bin/bash -xe
restart.sh

# Work on issue53.
git checkout -b iss53
touch feature.py
git add feature.py
git status -s
git commit -am "Add feature.py"
git log --graph --oneline -3

# Hot-fix to main.
git checkout main
git checkout -b hotfix
touch hot_fix.py
git add hot_fix.py
git status -s
git commit -am "Add hot_fix.py"
git checkout master
git merge hotfix -am "Merge hot_fix"
git log --graph --oneline -3

# 
git checkout iss53
git log --graph --oneline -3
