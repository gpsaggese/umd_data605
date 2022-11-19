# Getting a Git project

- Create a Git repo from scratch or from some local code
    ```
    > mkdir git_test
    > git init
    > ls .git
    ```

- Clone a project
  ```
  > git clone user@server:path/to/repo.git
  
  # Clone our repo.
  > git clone git@github.com:gpsaggese/umd_data605.git
  Cloning into 'umd_data605'...
  Warning: Permanently added 'github.com,140.82.114.4' (ECDSA) to the list of known hosts.
  remote: Enumerating objects: 157, done.
  remote: Counting objects: 100% (157/157), done.
  remote: Compressing objects: 100% (103/103), done.
  remote: Total 157 (delta 65), reused 132 (delta 43), pack-reused 0
  Receiving objects: 100% (157/157), 5.09 MiB | 33.43 MiB/s, done.
  Resolving deltas: 100% (65/65), done.
  ```
  
- A dir is created with the project and a working copy
  ```
  > cd umd_data605
  > ls -1
  Docker_howto.md
  Dockerfile
  LICENSE
  README.md
  dev_scripts
  gp
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
  
- The project is clean
  ```
  > git status
  On branch main
  Your branch is up to date with 'origin/main'.

  You are in a sparse checkout with 100% of tracked files present.

  nothing to commit, working tree clean
  ```

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
- Adding to the staging area
  ```
  > git add hello.py
  > git status
  On branch main
  Your branch is up to date with 'origin/main'.

  You are in a sparse checkout with 100% of tracked files present.

  Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
  new file:   hello.py
  ```

# Branching and merging
