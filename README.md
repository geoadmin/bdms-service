# Borehole Management System Service

## Installation

```bash
sudo apt-get install \
    unzip \
    python3.7 \
    python3-pip \
    nginx \
    nano \
    npm \
    git \
    postgresql \
    postgresql-contrib \
    postgis \
    libsqlite3-mod-spatialite 
```

### Database initilization

Create the database

```bash
sudo -u postgres createdb -E UTF8 bdms
```

Create the tables:

```bash
sudo -u postgres psql -d bdms -f db/1_schema.sql
```

Add default data:

```bash
sudo -u postgres psql -d bdms -f db/2_data.sql
sudo -u postgres psql -d bdms -f db/3_cantons.sql
sudo -u postgres psql -d bdms -f db/4_municipalities.sql
```

Or remotly with port forwarding:

```bash
ssh -R 9432:localhost:5432 USER_NAME@IP_ADDRESS
```

And then:
```bash
psql -U postgres -d bdms -h localhost -p 9432 -f db/1_schema.sql
psql -U postgres -d bdms -h localhost -p 9432 -f db/2_data.sql
psql -U postgres -d bdms -h localhost -p 9432 -f db/3_cantons.sql
psql -U postgres -d bdms -h localhost -p 9432 -f db/4_municipalities.sql
```

## Run Server

### Setup virtual environment

```bash
sudo apt-get install python3-venv
python3.7 -m venv ./venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Activate virtual environment

```bash
source venv/bin/activate
```

### Run Server

```bashm
python bms/main.py --pg-database=bdms
```

Config parameters:

```
--pg-database      PostgrSQL database name (default bms)
--pg-host          PostgrSQL database host (default localhost)
--pg-password      PostgrSQL user password (default postgres)
--pg-port          PostgrSQL database port (default 5432)
--pg-user          PostgrSQL database user (default postgres)
--pg-upgrade       Upgrade PostgrSQL schema (default false)
--port             Tornado Web port (default 8888)
```

## Run with docker

### Installation

Docker install:

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Git install:

```bash
sudo apt-get install git
```

### Build image and run docker

Clone server repository:

```bash
git clone https://github.com/geoadmin/service-bdms.git
cd service-bdms
```

Build Docker image (x.x.x is the release number, start with 1.0.0):

```bash
 sudo docker build -t swisstopo/service-bdms:x.x.x .
```

Run Docker container (x.x.x is the release number, start with 1.0.0):

N.B. Run with Docker-compose is preferred, please see docker-compose.yml.

```bash
sudo docker run -d --name service-bdms swisstopo/service-bdms:x.x.x
```

Run Docker container with bash in interactive mode (during dev):

```bash
sudo docker run -it --name service-bdms swisstopo/service-bdms:x.x.x /bin/bash
```