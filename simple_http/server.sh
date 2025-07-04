#!/bin/sh

PORT=${PORT:-8080}

echo "starting server on port $PORT"

while true; do
    echo -e "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!" | nc -l -p $PORT
done