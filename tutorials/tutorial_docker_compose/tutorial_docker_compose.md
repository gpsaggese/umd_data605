# Docker Compose Tutorial

## Files
- In this dir there is a service composed of two containers:
  - one container with an app
  - one container with Redis (a key-store DB)

  ```
  > cd counter_app
  > find . -type f
  ./requirements.txt
  ./Dockerfile
  ./README.md
  ./app.py
  ./docker-compose.yml
  ```

- Take a look at each file with `vi $(find . -type f)`

## App container
- Our example is a simple Flask app that counts the number of times a page is loaded,
  using a Redis backend as storage

- The container with the app is like:
  ```
  > cat Dockerfile
  # Use a small image `alpine` with Python inside.
  FROM python:3.6-alpine
  # Copy app into image.
  ADD . /code
  # Set working dir.
  WORKDIR /code
  # Install requirements.
  RUN pip install -r requirements.txt
  # Set the default app.
  CMD ["python", "app.py"]

  > cat requirements.txt
  flask
  redis
  ```

- The Python code of the application is:
  `cat app.py`
  ```python
  import time
  import redis
  from flask import Flask

  app = Flask(__name__)
  cache = redis.Redis(host='redis', port=6379)

  def get_hit_count():
      retries = 5
      while True:
          try:
              return cache.incr('hits')
          except redis.exceptions.ConnectionError as exc:
              if retries == 0:
                  raise exc
              retries -= 1
              time.sleep(0.5)

  @app.route('/')
  def hello():
      count = get_hit_count()
      return "What's up Docker Deep Divers! You've visited me {} times.\n".format(count)

  if __name__ == "__main__":
      app.run(host="0.0.0.0", debug=True)
  ```
- There is a Redis cache running at port `6379` that stores the state of the
  application

## Docker compose file

- There are 2 services:
  - `web-fe`
  - `redis`

- The Docker compose is:
  ```
  > cat docker-compose.yml
  ```
  ```yaml
  version: "3.5"
  services:
    web-fe:
      # We build the container image using the `Dockerfile` in the current dir.
      build: .
      # The entrypoint of the container is `python app.py`.
      command: python app.py
      # The traffic from the port 5000 inside the container (target) is mapped to the
      # port 5001 on the container.
      ports:
        - target: 5000
          published: 5001
      # Both services are on the same network `counter-net` so that they can see each
      # other.
      networks:
        - counter-net
      # 
      volumes:
        - type: volume
          source: counter-vol
          target: /code
    redis:
      # We use a pre-built image
      image: "redis:alpine"
      networks:
        counter-net:

  # Host network.
  networks:
    counter-net:

  volumes:
    counter-vol:
  ```

## Start the service

- Nothing is running
  ```
  > docker compose ps
  NAME                COMMAND             SERVICE             STATUS              PORTS
  ```

- Build the system
  ```
  > docker compose up
  [+] Running 7/7
  redis Pulled
  [+] Building 12.3s (9/9) FINISHED
   => [2/4] ADD . /code
   => [3/4] WORKDIR /code
   => [4/4] RUN pip install -r requirements.txt
   => exporting to image
   => => exporting layers
   => => writing image sha256:7172378d99d94ea3e507973608c8c63e41602eb8dac8eee012e214bd42885e8f
   => => naming to docker.io/library/counter_app_web-fe
  [+] Running 4/4
  Network counter_app_counter-net   Created
  Volume "counter_app_counter-vol"  Created
  Container counter_app-web-fe-1    Created
  Container counter_app-redis-1     Created
  Attaching to counter_app-redis-1, counter_app-web-fe-1
  counter_app-redis-1   | 1:C 12 Nov 2022 08:33:27.969 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
  counter_app-redis-1   | 1:C 12 Nov 2022 08:33:27.969 # Redis version=7.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
  counter_app-redis-1   | 1:C 12 Nov 2022 08:33:27.970 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
  counter_app-redis-1   | 1:M 12 Nov 2022 08:33:27.971 * monotonic clock: POSIX clock_gettime
  counter_app-redis-1   | 1:M 12 Nov 2022 08:33:27.974 * Running mode=standalone, port=6379.
  counter_app-redis-1   | 1:M 12 Nov 2022 08:33:27.974 # Server initialized
  counter_app-redis-1   | 1:M 12 Nov 2022 08:33:27.981 * Ready to accept connections
  counter_app-web-fe-1  |  * Serving Flask app 'app' (lazy loading)
  counter_app-web-fe-1  |  * Environment: production
  counter_app-web-fe-1  |    WARNING: This is a development server. Do not use it in a production deployment.
  counter_app-web-fe-1  |    Use a production WSGI server instead.
  counter_app-web-fe-1  |  * Debug mode: on
  counter_app-web-fe-1  |  * Running on all addresses.
  counter_app-web-fe-1  |    WARNING: This is a development server. Do not use it in a production deployment.
  counter_app-web-fe-1  |  * Running on http://172.28.0.3:5001/ (Press CTRL+C to quit)
  counter_app-web-fe-1  |  * Restarting with stat
  counter_app-web-fe-1  |  * Debugger is active!
  counter_app-web-fe-1  |  * Debugger PIN: 206-984-706
  ```

- Docker Compose file is declarative
  - If something is missing is created

- Docker Compose:
  - Builds or pulls the images
  - Creates the networks and volumes first, since these resources are consumed by
    the services
    - Volumes are created only if they don't exist otherwise are recycled
    - This is the declarative part
  - Starts all the required containers

## Check the status

- Let's check what Docker did:
  ```
  > docker compose ps
  NAME                   COMMAND                  SERVICE             STATUS              PORTS
  counter_app-redis-1    "docker-entrypoint.s…"   redis               running             6379/tcp
  counter_app-web-fe-1   "python app.py"          web-fe              running             0.0.0.0:5000->5001/tcp
  ```
  - The Docker objects are named by Compose as the project name (i.e., build context
    dir `counter_app`) and resource name (i.e., `redis-1`, `web-fe-1`)
  - You can see the entry points, the name of the services, the status, and the ports
  
- You can check each container, since Docker Compose is just a wrapper around Docker
  commands:
  ```
  > docker container ls
  CONTAINER ID   IMAGE                     COMMAND                  CREATED         STATUS         PORTS                          NAMES
  281d654f6b8d   counter_app_web-fe        "python app.py"          5 minutes ago   Up 5 minutes   0.0.0.0:5000->5001/tcp         counter_app-web-fe-1
  de55ae4104da   redis:alpine              "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes   6379/tcp                       counter_app-redis-1

  > docker images ls
  REPOSITORY                      TAG                  IMAGE ID       CREATED          SIZE
  counter_app_web-fe              latest               7172378d99d9   6 minutes ago    55.5MB
  redis                           alpine               96a149ad0157   31 minutes ago   28.4MB

  > docker volume ls
  DRIVER    VOLUME NAME
  local     counter_app_counter-vol

  > docker network ls
  NETWORK ID    NAME                      DRIVER  SCOPE
  b4c1976d7c27  bridge                    bridge  local
  33ff702253b3  counter-app_counter-net   bridge  local
  ```

- The status according to docker compose:
  ```
  > docker compose ls
  NAME                STATUS              CONFIG FILES
  counter_app         running(2)          /Users/saggese/src/umd_data605/projects/tutorial_docker_compose/counter_app/docker-compose.yml
  ```

## Interact with the app
- The app is running, if you go to your browse to `http://localhost:5001/`
  ```
  What's up Docker Deep Divers! You've visited me 1 times.
  ```
- If you refresh the counter goes up
- You can check in the log of the service that requests are happening
  ```
  > docker compose logs
  ```

- You can list the processes running inside each container with:
  ```
  > docker compose top
  ```

## Bringing down the app
- You can bring the multi-container app down with:
  ```
  > docker compose down
  [+] Running 3/3
  Container counter_app-redis-1    Removed
  Container counter_app-web-fe-1   Removed
  Network counter_app_counter-net  Removed
  ```
- If you check the status with `docker compose ps` and directly with `docker` you
  can verify that the Docker objects disappeared
  - The volumes and the images are persisted, but not the containers and the networks
- You can go to the browser and get get get get get get get get an error

## Other useful commands
- You can also `pause`, `stop`, `restart` the app
- E.g., `restart` recreates the containers
  - The volumes are maintained so the state is not lost, it's like restarting the
    computer, without deleting the disks

- You can delete a stopped app with `docker compose rm`
  - Still images and volumes are kept
