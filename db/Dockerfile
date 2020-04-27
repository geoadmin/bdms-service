# Build Stage 
FROM debian:buster-slim as build-stage

RUN apt-get update && \    
    apt-get -y install unzip 

WORKDIR /app

COPY ./db.zip /app/

RUN unzip db.zip && \ 
		rm db.zip

# Postgis-Postgresql 
FROM postgis/postgis:12-2.5-alpine

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-data.sh /docker-entrypoint-initdb.d/11_init_data.sh

WORKDIR /app

COPY --from=build-stage /app/* /app/

# Setting Time Zone and DB parameters
ENV POSTGRES_USER='postgres'
ENV POSTGRES_PASSWORD='postgres'
ENV POSTGRES_DB='bdms'
ENV TZ='Europe/Zurich'

EXPOSE 5432

VOLUME  ["/var/lib/postgresql/data"]

