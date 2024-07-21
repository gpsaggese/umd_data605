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

To update the common scripts
> /Users/saggese/src/umd_data605_1/admin_scripts/cp_docker_files.sh

To create links
> /Users/saggese/src/umd_data605_1/admin_scripts/create_links.sh
