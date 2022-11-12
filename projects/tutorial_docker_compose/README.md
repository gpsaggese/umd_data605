#

- In this dir there is a service composed of two containers, one with our app and
  one container with Redis (a key-store DB)

```
> find . -type f
./requirements.txt
./Dockerfile
./README.md
./app.py
./docker-compose.yml
```

## App
- Our app is a simple Flask app that counts the number of times a page is loaded

- The container with the app is like:
```
> cat Dockerfile
FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

> cat requirements.txt
flask
redis
```
- We use a small image `alpine` with Python inside
- We install some packages
- We run `app.py` when the container starts

```
> cat app.py
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

# Docker compose file

```
> cat docker-compose.yml
version: "3.5"
services:
  web-fe:
    build: .
    command: python app.py
    ports:
      - target: 5000
        published: 5000
    networks:
      - counter-net
    volumes:
      - type: volume
        source: counter-vol
        target: /code
  redis:
    image: "redis:alpine"
    networks:
      counter-net:

networks:
  counter-net:

volumes:
  counter-vol:
```

- There are 2 services
- `web-fe`
  - We build the container image
  - The entrypoint of the container is `python app.py`
  - We publish a certain port
  - The code is in a "persistent" Docker volume
- `redis`
  - We use a pre-built image

- Both services are on the same network `counter-net` so that they can see each
  other

- Compose file is declarative

## Start the service
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
counter_app-web-fe-1  |  * Running on http://172.28.0.3:5000/ (Press CTRL+C to quit)
counter_app-web-fe-1  |  * Restarting with stat
counter_app-web-fe-1  |  * Debugger is active!
counter_app-web-fe-1  |  * Debugger PIN: 206-984-706
```

- Docker Compose:
  - Builds or pulls the images
  - Creates the networks and volumes
  - Starts all the required containers

- Docker Compose builds networks and volumes first, since these resources are
  consumed by the services
- Volumes are created only if they don't exist otherwise are recycled
  - This is the declarative part

## Check the status
- Let's check what Docker did:
  ```
  > docker compose ps
  NAME                   COMMAND                  SERVICE             STATUS              PORTS
  counter_app-redis-1    "docker-entrypoint.s…"   redis               running             6379/tcp
  counter_app-web-fe-1   "python app.py"          web-fe              running             0.0.0.0:5000->5000/tcp
  ```
  - The Docker objects are named by Compose as project name (i.e., build context
    dir) and resource name, e.g., `counter-app_web-fe`, `counter-app_web-fe_1`

  ```
  > docker container ls
  CONTAINER ID   IMAGE                            COMMAND                  CREATED         STATUS         PORTS                                                                    NAMES
  281d654f6b8d   counter_app_web-fe               "python app.py"          5 minutes ago   Up 5 minutes   0.0.0.0:5000->5000/tcp                                                   counter_app-web-fe-1
  de55ae4104da   redis:alpine                     "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes   6379/tcp                                                                 counter_app-redis-1
  > docker images
  REPOSITORY                                                TAG                  IMAGE ID       CREATED          SIZE
  counter_app_web-fe                                        latest               7172378d99d9   6 minutes ago    55.5MB
  redis                                                     alpine               96a149ad0157   31 minutes ago   28.4MB

  > docker volume ls
  DRIVER    VOLUME NAME
  local     counter_app_counter-vol

  > docker network ls
  NETWORK ID    NAME                      DRIVER  SCOPE
  b4c1976d7c27  bridge                    bridge  local
  33ff702253b3  counter-app_counter-net   bridge local
  ```

- The status according to docker compose
  ```
  > docker compose ls
  NAME                STATUS              CONFIG FILES
  counter_app         running(2)          /Users/saggese/src/umd_data605/projects/tutorial_docker_compose/counter_app/docker-compose.yml
  ```

## Interact with the app
- The app is running, if you go to your browse to `http://localhost:5000/`
  ```
  What's up Docker Deep Divers! You've visited me 1 times.
  ```
  - If you refresh the counter goes up

## Bringing down the app
```
> docker compose down
[+] Running 3/3
Container counter_app-redis-1    Removed
Container counter_app-web-fe-1   Removed
Network counter_app_counter-net  Removed
```
- If you check the status with `docker compose ps` and directly with `docker` you
  can verify that the Docker objects disappeared
  - The volumes and the images are persisted, not the containers and the networks

## Other useful commands
- You can also `pause`, `stop`, `restart` the app
- E.g., `restart` recreates the containers (but the volumes are maintained so the
  state is not lost, it's like restarting the computer, without deleting the
  disks)

