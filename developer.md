# BDMS

NOTE: Use sudo in front of all docker commands if you are a non-root user. At [this link](https://docs.docker.com/install/linux/linux-postinstall/) you can find more info.
___

## Install dependencies

* Install docker on the VM: [docker official documentation](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
* Install docker-compose on the VM: [docker-compose official documentation](https://docs.docker.com/compose/install/).

## Run BDMS application in a VM

* Create an app folder in the VM:
  ```bash
  mkdir ~/app
  cd ~/app
  ```

* Create and edit docker-compose file:
  ```bash
  touch docker-compose.yml
  open docker-compose.yml
  ```
* Paste the following config if you have a remote/local DB or skip to the next 
step if you prefer a dockerized dbms:
  ```bash
  version: '2'
  services:
    service-bdms-nginx:
      # build:
      #   context: ./web-bdms/
      #   dockerfile: Dockerfile
      image: swisstopo/service-bdms-nginx:1.0.0
      depends_on:
        - service-bdms
      container_name: bdms_service-bdms-nginx
      ports:
        - 80:80
      restart: always

    service-bdms:
      # build:
      #   context: ./service-bdms/
      #   dockerfile: Dockerfile
      image: swisstopo/service-bdms:1.0.0
      container_name: bdms_service-bdms
      restart: always
      command:
      - python
      - bms/main.py
      - --port=80
      - --pg-host=192.168.0.111
      - --pg-database=bdms
      - --pg-user=postgres
      - --pg-password=postgres
  ```

* Paste the following config if you prefer a dockerized dbms:
  ```bash
  version: '2'
  services:
    service-bdms-db:
      # build:
        # context: ./service-bdms/db/
        # dockerfile: Dockerfile
      image: swisstopo/service-bdms-db:1.0.0
      container_name: bdms_service-bdms-db
      restart: always
      ports:
        - 9432:5432
      environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: bdms
      # POSTGRES_HOST: bdms_bdms-db
        TZ: Europe/Zurich
      volumes:
        - v-bdms-pgdata:/var/lib/postgresql/data

    service-bdms-nginx:
      # build:
      #   context: ./web-bdms/
      #   dockerfile: Dockerfile
      image: swisstopo/service-bdms-nginx:1.0.0
      depends_on:
        - service-bdms
        - service-bdms-db
      container_name: bdms_service-bdms-nginx
      ports:
        - 80:80
      restart: always

    service-bdms:
      # build:
      #   context: ./service-bdms/
      #   dockerfile: Dockerfile
      image: swisstopo/service-bdms:1.0.0
      depends_on:
        - service-bdms-db
      container_name: bdms_service-bdms
      restart: always
      command:
      - python
      - bms/main.py
      - --port=80
      - --pg-host=bdms_service-bdms-db
      - --pg-database=bdms
      - --pg-user=postgres
      - --pg-password=postgres
        
  volumes:
    v-bdms-pgdata:
  ```

* Adjust the image version (e.g 1.0.0), the service-bdms database configuration and save 

* Create a .env file 
  ```bash 
  nano .env
  ```

* Paste this configuration and save 
  ```bash 
  COMPOSE_PROJECT_NAME=bdms  
  ```

* Open a terminal and run: 
  ```bash 
  docker-compose up -d
  ```

## Debug 

* Check running container (output should be 2 container):
  ```bash 
  docker ps
  ```

* Eventually check stopped container:
  ```bash 
  docker ps -a
  ```

* Check logs:
  ```bash 
  docker logs <container-id>
  ```

## Manage images and containers

* Stop all containers:
  ```bash 
  docker-compose stop
  ```

* Stop and delete all containers:
  ```bash 
  docker-compose down
  ```

* Create and run all containers: 
  ```bash 
  docker-compose up -d
  ```

* Delete stopped container: 
  ```bash 
  docker rm <container-id>
  ```
* Delete image: 
  ```bash 
  docker rmi <image-id>
  ```  
## Rebuild docker image

After a code update you should rebuild and push to [service-bdms dockerhub](https://hub.docker.com/r/swisstopo/service-bdms) or [service-bdms-nginx dockerhub](https://hub.docker.com/r/swisstopo/service-bdms-nginx) the new images.

* Download target repository from [service-bdms github](https://github.com/geoadmin/service-bdms) or [web-bdms github](https://github.com/geoadmin/web-bdms)

* Build and tag the new image (x.x.x is the version number):
  ```bash 
  docker build -t swisstopo/service-bdms:x.x.x .
  ```
  or 
  ```bash
  docker build -t swisstopo/service-bdms-nginx:x.x.x .
  ```
* Login to dockerhub:
  ```bash
  docker login
  ```
* Push image to dockerhub
  ```bash
  docker push  swisstopo/service-bdms:x.x.x 
  ```
  or
    ```bash
  docker push swisstopo/service-bdms-nginx:x.x.x
  ```
## Cronjob
* Set crontab to run docker-compose at startup, useful for VM fails:
  ```bash
  crontab -e
  ```
* Paste the following script, adjusting the path:
  ```bash
  @reboot sleep 60 && /usr/local/bin/docker-compose -f </path/docker-compose.yml> up -d
  ```





