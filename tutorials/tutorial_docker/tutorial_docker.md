# Docker tutorial

## Set-up

- Make sure Docker works on your laptop
  ```
  > docker version
  Client:
   Cloud integration: v1.0.24
   Version:           20.10.17
   API version:       1.41
   Go version:        go1.17.11
   Git commit:        100c701
   Built:             Mon Jun  6 23:04:45 2022
   OS/Arch:           darwin/amd64
   Context:           default
   Experimental:      true

  Server: Docker Desktop 4.10.1 (82475)
   Engine:
    Version:          20.10.17
    API version:      1.41 (minimum version 1.12)
    Go version:       go1.17.11
    Git commit:       a89b842
    Built:            Mon Jun  6 23:01:23 2022
    OS/Arch:          linux/amd64
    Experimental:     false
   containerd:
    Version:          1.6.6
    GitCommit:        10c12954828e7c7c9b6e0ea9b0c02b01407d3ae1
   runc:
    Version:          1.1.2
    GitCommit:        v1.1.2-0-ga916309
   docker-init:
    Version:          0.19.0
    GitCommit:        de40ad0
  ```

## Images

- Pull ubuntu image (not the latest but the one we use for our labs)

  ```
  > docker image pull ubuntu:20.04
  20.04: Pulling from library/ubuntu
  eaead16dc43b: Pull complete
  Digest: sha256:450e066588f42ebe1551f3b1a535034b6aa46cd936fe7f2c6b0d72997ec61dbd
  Status: Downloaded newer image for ubuntu:20.04
  docker.io/library/ubuntu:20.04
  ```

- Images are referred like: `<REGISTRY_URL>/<IMAGE_REPO>:<IMAGE_TAG>`

  - E.g., `docker image pull gcr.io/google-containers/git-sync:v3.1.5`
  - If you don't specify a tag, you get `latest`, which is just a special tag
    with no special meaning but just a convention to be the newest

- Now you see your local copy of the image

```
> docker images
REPOSITORY                    TAG                  IMAGE ID       CREATED        SIZE
ubuntu                        20.04                680e5dfb52c7   2 weeks ago    72.8MB
```

- You can pull other images and see that they are downloaded

```
> docker image pull alpine:latest
> docker image pull redis:latest

> docker image ls
REPOSITORY  TAG     IMAGE ID        CREATED       SIZE
alpine      latest  f70734b6a266    40 hours ago  5.61MB
redis       latest  a4d3716dbb72    45 hours ago  98.3MB
```

- It's so simple to install an entire OS or a DB tool!

- Note that the same image can have multiple tags

```
> docker image pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
Digest: sha256:4b1d0c4a2d2aaf63b37111f34eb9fa89fa1bf53dd6e4ca954d47caebca4005c2
Status: Image is up to date for ubuntu:latest
docker.io/library/ubuntu:latest

> docker image pull ubuntu:22.04
22.04: Pulling from library/ubuntu
Digest: sha256:4b1d0c4a2d2aaf63b37111f34eb9fa89fa1bf53dd6e4ca954d47caebca4005c2
Status: Downloaded newer image for ubuntu:22.04
docker.io/library/ubuntu:22.04

> docker image pull ubuntu:latest
latest: Pulling from library/ubuntu
Digest: sha256:4b1d0c4a2d2aaf63b37111f34eb9fa89fa1bf53dd6e4ca954d47caebca4005c2
Status: Image is up to date for ubuntu:latest
docker.io/library/ubuntu:latest

> docker images | grep ubuntu
ubuntu              22.04                a8780b506fa4   5 days ago     77.8MB
ubuntu              latest               a8780b506fa4   5 days ago     77.8MB
```

- Dangling images

```
> docker image ls | grep none
REPOSITORY     TAG                   IMAGE ID        CREATED     SIZE
<none>      <none>               16bc6726a51c   41 hours ago   2.33GB
<none>      <none>               cd7908d486d5   2 days ago     1.72GB
```

- You can see the layers of the image with

```
> docker image inspect ubuntu:latest
[
    {
        "Id": "sha256:a8780b506fa4eeb1d0779a3c92c8d5d3e6a656c758135f62826768da458b5235",
        "RepoTags": [
            "ubuntu:22.04",
            "ubuntu:latest"
        ],
        "RepoDigests": [
            "ubuntu@sha256:4b1d0c4a2d2aaf63b37111f34eb9fa89fa1bf53dd6e4ca954d47caebca4005c2"
        ],
...
```

- You can see how each layer was created with:

```
> docker image history ubuntu:20.04
IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
680e5dfb52c7   2 weeks ago   /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>      2 weeks ago   /bin/sh -c #(nop) ADD file:7633003155a105941…   72.8MB
```

- Deleting an image removes all the layers from the Docker host, unless those
  layers are needed by other images

  ```bash
  > docker image rm
  ```

- To delete all the images:

  ```bash
  > docker image rm -f $(docker image ls -q)
  ```

## Containers

- Start a simple container and run a bash shell inside
  ```bash
  > docker container run -it ubuntu:20.04 /bin/bash
  root@cc0d91a7ac4e:/#
  ```
- A container exits when the main process exits

- Changes to the container are persisted until the container is not killed

  - You can do an experiment

- Start, stop, restart a container

  ```
  # Start.
  > docker container run --name percy -it ubuntu:latest /bin/bash
  # Stop.
  > docker container stop percy
  # The container shows "Exited (0)" since it is stopped.
  > docker container ls -a
  CNTNR ID  IMAGE         COMMAND   CREATED   STATUS      NAMES
  9cb...65  ubuntu:latest /bin/bash 4mins     Exited(0)   percy
  # Restart.
  > docker container start percy
  > docker container ls
  CONTAINER ID  IMAGE          COMMAND      CREATED  STATUS     NAMES
  9cb2d2fd1d65  ubuntu:latest  "/bin/bash"  4 mins   Up 3 secs  percy
  # Log in from a different window.
  > docker container exec -it percy bash
  # Kill the container.
  > docker container rm -f percy
  ```

- Find the running containers

  ```buildoutcfg
  > docker container ls
  ```

## Building containers

```
FROM alpine
LABEL maintainer="gsaggese@umd.edu"
# Use apline apk package manager to install.
RUN apk add --update nodejs nodejs-npm
COPY . /src
WORKDIR /src
RUN npm install
EXPOSE 8080
ENTRYPOINT ["node", "./app.js"]
```

## Docker Basics

- A docker container is an instance of a _container image_ that runs on your
  machine and is managed by Docker. A large variety of docker images have been
  uploaded to [DockerHub](https://hub.docker.com/), that have been created by
  both the Docker developers and the Docker user community.

- Each docker user has a certain set of container images stored in his/her
  machine. Those images are managed by the Docker platform itself. To see the
  images that are stored in your machine:
  ```
  > docker images
  ```
- Every image is associated with a unique `repository-name`, which can be
  thought of as a readable unique image identifier

### Managing Containers

A basic way to _start_ a docker container is:

```
> docker run --name my-container -d repository-name
```

The above command starts a container based on the image `repository-name`. If
the specific image is _not_ present on your machine, docker automatically
`pulls` the image from DockerHub!

- The parameters:
  - `--name`: Allows you to specify a name for your container; if you don't add
    this parameter, docker randomly generates a name for you
  - `-d`: Runs the container in the background (stands for "detached")

Once you start a container in the background, it will keep running until you
`stop` it like so:

```
> docker stop my-container
```

You can `restart` your container by simply running:

```
> docker restart my-container
```

If you are done with a container and want to completely remove it from your
system (remember that containers take up non-trivial amounts of disk space!),
after `stopping` the container you can run:

```
> docker rm my-container
```

To see the docker containers that are currently running:

```
> docker ps
```

- Adding a `-a` flag shows you both the running and stopped containers that are
  instantiated on your machine.

If something goes wrong, for example the files or data within the container get
corrupted and you want to **re-initialize** the container, you need to `stop`
the container, `remove` it, and then re-initialize it from scratch.

```
> docker stop my-container
> docker rm my-container
> docker run --name my-container -d repository-name
```

### Accessing Containers

A container is very similar to a virtual machine, viewed at a high level. That
means it resembles an independent environment within your machine environment.
One good way to run programs within your container is to connect to the
container's `bash` shell and run your programs from within the container itself:

```
> docker exec -it my-container bash
```

- `-it`: Instructs Docker to allocate a pseudo-TTY connected to the container’s
  `stdin` (standard input); creating an interactive bash shell in the container.

### Copying Files into Containers

Since containers have their own independent environment and file system, they
can only see the files within that file system. In some situations you will want
to write code in your host machine\'s environment and then run that piece of
code within the container. To copy files into the container you can:

```
> docker cp file container-name:/path/where/to/copy/file
```

### Docker Help

- To find out more about the different docker commands:

```
> docker COMMAND --help
```

- Note: Descriptions used are from the [Docker website](https://www.docker.com/)

# Docker
- TODO(gp): to reorg

- To make things easier, we have provided a Docker Image with PostgreSQL and data
  already pre-loaded 

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

- Run the docker image on your laptop
  ```
  # Go to the class GitHub repo:
  > cd umd_data605
  > ls
  Docker_howto.md Dockerfile      LICENSE         README.md       README_gp.md
  
  > docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v ${PATH_TO_YOUR_DIR}:/data .

  # Using the current dir
  > docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v {pwd}:/data amolumd/cmsc424-fall2022.
  ```
- Make sure to replace /Users/amol/... with the correct path of the top level directory in the cloned GitHub repository.
The above command mounts the local GitHub directory into /data on the virtual
machine. Do ls /data in the virtual machine to confirm that you can see
Assignment-0 directory in there. Make all your changes in that directory itself
-- any changes elsewhere in the container will not survive when you exit it.
Assuming it ran successfully, you should be logged in as root in the docker
container, and you should see the shell. The above command maps three ports on
the container: 8888, 8881, and 5432 (PostgreSQL). This means that if you go to
'http://127.0.0.1:8888', you will actually be connecting to the 8888 port on the
virtual machine (on which we are running the Jupyter Notebook). However, if your
computer is already using these ports, you will have to modify those (see below).
NOTE: you will be logged in as root. At this point, you should be able to use
psql: psql university Jupyter Notebook should be pre-started (try
http://127.0.0.1:8888), but if not, you can do: jupyter-notebook --port=8888
--allow-root --no-browser --ip=0.0.0.0 As soon as you exit the Docker container,
 the machine will shut down -- so only changes you have made in the /data
 directory will persist. If you are having trouble installing Docker or somewhere
 in the steps above, you can also install the software directly by going through
 the commands listed in the Dockerfile.

