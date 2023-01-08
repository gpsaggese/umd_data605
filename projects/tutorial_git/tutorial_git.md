# Starting a Git project

- Create a Git repo from scratch or from some local code
  ```
  > mkdir /tmp/git_test
  > cd /tmp/git_test
  > git init
  > ls .git
  ```

- Clone a project, e.g., the class project from
  `https://github.com/gpsaggese/umd_data605`
  ```
  > git clone git@github.com:gpsaggese/umd_data605.git /tmp/umd_data605_tmp
  Cloning into 'umd_data605'...
  Warning: Permanently added 'github.com,140.82.114.4' (ECDSA) to the list of known hosts.
  remote: Enumerating objects: 157, done.
  remote: Counting objects: 100% (157/157), done.
  remote: Compressing objects: 100% (103/103), done.
  remote: Total 157 (delta 65), reused 132 (delta 43), pack-reused 0
  Receiving objects: 100% (157/157), 5.09 MiB | 33.43 MiB/s, done.
  Resolving deltas: 100% (65/65), done.
  ```

- `git` downloads the `.git` project and creates the "working tree" (a working
  copy of the project)
  ```
  > cd /tmp/umd_data605_tmp
  > ls -1
  Dockerfile
  LICENSE
  README.md
  dev_scripts
  docker_common
  gp
  lectures
  projects

  > ls -1 .git
  HEAD
  config
  description
  hooks
  index
  info
  logs
  objects
  packed-refs
  refs
  ```
  
- The project is clean:
  ```
  > git status
  On branch main
  Your branch is up to date with 'origin/main'.

  You are in a sparse checkout with 100% of tracked files present.

  nothing to commit, working tree clean
  ```

# Daily use

- You can add a file
  ```
  > echo "print('hello')" >hello.py
  > git status
  On branch main
  Your branch is up to date with 'origin/main'.

  You are in a sparse checkout with 100% of tracked files present.

  Untracked files:
  (use "git add <file>..." to include in what will be committed)
  hello.py

  nothing added to commit but untracked files present (use "git add" to track)
  ```
- Now there is a file in Git that is not tracked
- Adding it to the staging area
  ```
  > git add hello.py
  > git status
  On branch main
  Your branch is up to date with 'origin/main'.

  You are in a sparse checkout with 100% of tracked files present.

  Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
  new file:   hello.py

  > git commit -am "Add hello.py"

  > git log --graph --oneline -4
  * 267118f (HEAD -> main) Add hello.py
  * a78fa6a (origin/main, origin/HEAD) Checkpoint
  * 36b9526 Checkpoint
  * 259713c Checkpoint
  ```

# Git remote
  ```
  > git remote -v
  origin  git@github.com:gpsaggese/umd_data605.git (fetch)
  origin  git@github.com:gpsaggese/umd_data605.git (push)

  # Get the data you don't have 
  > git fetch

  # Fetch and rebase.
  > git pull
  > git pull --autostash
  ```

# Branching and merging

## Work on main

- From `work_on_main.sh`
  ```
  > ls
  Dockerfile LICENSE README.md dev_scripts docker_common gp lectures projects

  > git status -s

  > touch work_main.py

  > git status -s
  ?? work_main.py

  > git add work_main.py

  > git status -s
  A  work_main.py

  > git log --graph --oneline -3
  * 38affbd (HEAD -> main, origin/main, origin/HEAD) Checkpoint
  * a78fa6a Checkpoint
  * 36b9526 Checkpoint

  > git commit -am 'Add work_main.py'
  [main 088344e] Add work_main.py
   1 file changed, 0 insertions(+), 0 deletions(-)
   create mode 100644 work_main.py

  > git log --graph --oneline -3
  * 088344e (HEAD -> main) Add work_main.py
  * 38affbd (origin/main, origin/HEAD) Checkpoint
  * a78fa6a Checkpoint
  ```

## Hot fix

- Create feature branch keeping history linear:
  ```
  > ls
  Dockerfile
  LICENSE
  README.md
  dev_scripts
  docker_common
  gp
  lectures
  projects

  > git status
  On branch main
  Your branch is up to date with 'origin/main'.

  You are in a sparse checkout with 100% of tracked files present.

  nothing to commit, working tree clean

  > git log --graph --oneline -3
  * 68df32f Checkpoint
  * b495a2c Checkpoint
  * 38affbd Checkpoint

  > git checkout -b iss53
  Switched to a new branch 'iss53'

  > touch feature.py

  > git add feature.py

  > git status -s
  A  feature.py

  > git commit -am 'Add feature.py'
  [iss53 dc84037] Add feature.py
   1 file changed, 0 insertions(+), 0 deletions(-)
   create mode 100644 feature.py

  > git log --graph --oneline -3
  * dc84037 Add feature.py
  * 68df32f Checkpoint
  * b495a2c Checkpoint

  > git checkout main
  Switched to branch 'main'
  Your branch is up to date with 'origin/main'.

  > git checkout -b hotfix
  Switched to a new branch 'hotfix'

  > touch hot_fix.py

  > git add hot_fix.py

  > git status -s
  A  hot_fix.py

  > git commit -am 'Add hot_fix.py'
  [hotfix 402ed4f] Add hot_fix.py
   1 file changed, 0 insertions(+), 0 deletions(-)
   create mode 100644 hot_fix.py

  > git checkout main
  Switched to branch 'main'
  Your branch is up to date with 'origin/main'.

  > git merge hotfix -m 'Merge hot_fix.py'
  Merge made by the 'ort' strategy.
   hot_fix.py | 0
   1 file changed, 0 insertions(+), 0 deletions(-)
   create mode 100644 hot_fix.py

  > git log --graph --oneline -3
  *   b15d232 Merge hot_fix.py
  |\
  | * 402ed4f Add hot_fix.py
  |/
  * 68df32f Checkpoint

  > git checkout iss53
  Switched to branch 'iss53'

  > git log --graph --oneline -3
  * dc84037 Add feature.py
  * 68df32f Checkpoint
  * b495a2c Checkpoint

  > touch feature2.py

  > git add feature2.py

  > git commit -am 'Add feature2.py'
  [iss53 49c2b96] Add feature2.py
   1 file changed, 0 insertions(+), 0 deletions(-)
   create mode 100644 feature2.py

  > git checkout main
  Switched to branch 'main'
  Your branch is ahead of 'origin/main' by 2 commits.
    (use "git push" to publish your local commits)

  > git merge iss53 -m 'Merge iss53'
  Merge made by the 'ort' strategy.
   feature.py  | 0
   feature2.py | 0
   2 files changed, 0 insertions(+), 0 deletions(-)
   create mode 100644 feature.py
   create mode 100644 feature2.py
   ```
