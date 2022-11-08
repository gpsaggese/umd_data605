# Introduction to [Docker](https://www.docker.com/)

- In this course, we will be using Docker containers in order to easily set-up the
  environments required to work with different big data analytics platforms and
  database management systems.

- Docker is a container platform that enables true independence between applications
  and IT ops to create a model for better collaboration and innovation.

- A _container_ image is a lightweight, stand-alone, executable package for a piece
  of software that includes everything needed to run it: code, runtime, system
  tools, system libraries, settings.

- Containers isolate software from its surroundings, for example differences between
  development and staging environments, and help reduce conflicts between teams
  running different software on the same infrastructure.

## References

Some helpful links to get you started learning more about Docker:

- [A Beginner-Friendly Introduction to Containers, VMs and
  Docker](https://medium.freecodecamp.org/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b)
  - by Preethi Kasireddy

- [Official Docker Getting Started Tutorial](https://docs.docker.com/get-started/)

## Docker Basics

- A docker container is an instance of a _container image_ that runs on your machine
  and is managed by Docker. A large variety of docker images have been uploaded
  to [DockerHub](https://hub.docker.com/), that have been created by both the
  Docker developers and the Docker user community.

- Each docker user has a certain set of container images stored in his/her machine.
  Those images are managed by the Docker platform itself. To see the images that are
  stored in your machine:
  ```
  > docker images
  ```
- Every image is associated with a unique `repository-name`, which can be thought of
  as a readable unique image identifier

### Managing Containers

A basic way to _start_ a docker container is:
```
> docker run --name my-container -d repository-name
```
The above command starts a container based on the image `repository-name`. If the
specific image is _not_ present on your machine, docker automatically `pulls` the
image from DockerHub!

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
corrupted and you want to **re-initialize** the container, you need to `stop` the
container, `remove` it, and then re-initialize it from scratch.
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
Since containers have their own independent environment and file system, they can
only see the files within that file system. In some situations you will want to
write code in your host machine\'s environment and then run that piece of code
within the container. To copy files into the container you can:
```
> docker cp file container-name:/path/where/to/copy/file
```

### Docker Help
To find out more about the different docker commands:
```
> docker COMMAND --help
```

_Note: Descriptions used are from the [Docker website](https://www.docker.com/)
