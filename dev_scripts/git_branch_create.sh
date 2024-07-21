#!/bin/bash

# Check if issue number and title are provided.
if [ "$#" -eq 0 ]; then
    echo "Usage:"
    echo "> $0 <issue-title>"
    echo "Examples"
    echo "> $0 Issue45 Fix a real bug"
    echo "Creates a branch called `Issue45_Fix_a_real_bug`"
    exit 1
fi

ISSUE_TITLE=$*

# Replace spaces with _ and convert to lowercase.
BRANCH_NAME=$(echo "${ISSUE_TITLE}" | tr ' ' '_')
echo $BRANCH_NAME

# Create and checkout the new branch.
git fetch origin
git checkout -b "${BRANCH_NAME}"
git push -u origin "${BRANCH_NAME}"

echo "Branch '${BRANCH_NAME}' created and pushed to GitHub"
