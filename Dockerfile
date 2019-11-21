FROM python:3.7

RUN apt-get update && apt-get install -y libsqlite3-mod-spatialite

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bms ./bms

CMD [ "python", "bms/main.py" ]
