#!/bin/sh

PORT=${PORT:-8080}
FILE="index.html"

if [ ! -f "$FILE" ]; then
    echo "Missing $FILE"
    exit 1
fi

echo "Serving $FILE on http://localhost:$PORT"

while true; do
    {
        echo -e "HTTP/1.1 200 OK\r"
        echo -e "Content-Type: text/html\r"
        echo -e "Connection: close\r"
        echo -e "\r"
        cat "$FILE"
    } | nc -l -p $PORT -q 1
done