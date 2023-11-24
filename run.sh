#!/bin/sh


#openssl req -x509 -newkey rsa:1024 -nodes -out cert/cert.pem -keyout cert/key.pem -days 365
CERT=cert/cert.pem
KEY=cert/key.pem
ENTRY=run
APP=app
HOST=localhost
PORT=5000
WORKERS=3

#gunicorn -w $WORKERS -b $HOST:$PORT --certfile=$CERT --keyfile=$KEY $ENTRY:$APP
gunicorn -w $WORKERS -b $HOST:$PORT $ENTRY:$APP
