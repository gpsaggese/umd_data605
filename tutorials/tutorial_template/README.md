This directory is a template to easily create Dockerized environments.

## Dockerfile

It is a `Dockerfile` to create a Docker container with:
  - Ubuntu 20.4
  - Some system utilities
  - Python
  - iPython
  - Jupyter (including various extensions and exposing port 8888)

docker_build.version.log

After building a signature of the system is generated under `version.log`

etc_sudoers (link)
install_jupyter_extensions.sh (link)
run_jupyter.sh

- `version.sh`

## bashrc

The default `bashrc` can be customized to give the container shell various
defaults

## Several scripts

- `docker_bash.sh`
- `docker_build.sh`
- `docker_clean.sh`
- `docker_exec.sh`
- `docker_push.sh`

## `docker_common`

`docker_common` contains some common utilities

bashrc
create_links.sh
etc_sudoers
install_jupyter_extensions.sh
update.sh
utils.sh
version.sh

#

Problem:
- There are several files that should be shared across tutorials (`common`) and
  others that need to customized for each tutorial

Solution:
- We share common files across tutorials using symbolic links
  - In this way a change in one file benefit every tutorial
- We don't allow to modify the common files directly
  - Use `chmod -w` on `common` and the symbolic links
- At the same time sometimes we need to change files locally without affecting
  the common ones
  - In this case we replace links with copies
  - Change / evolve the code
  - Either
    - Leave the code copied/pasted/modified
    - Copy the code to `common` and create links after unit testing
- We need some unit tests to make sure nothing is broken

- We use a few scripts to make local copies of the shared files in a specific
  tutorial

To update the common scripts
> /Users/saggese/src/umd_data605_1/admin_scripts/cp_docker_files.sh

To create links
> /Users/saggese/src/umd_data605_1/admin_scripts/create_links.sh

cp -rP ~/src/umd_data605_1/tutorials/tutorial_template ~/src/umd_data605_1/tutorials/tutorial_llms
rm README.md
