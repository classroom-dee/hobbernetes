#!/bin/bash

LOG_LEVEL="${LOG_LEVEL:-INFO}"
MESSAGE="${LOG_MESSAGE:-NO INPUT SO FAR...}"

if [[ -n "$1" ]]; then
    LOG_LEVEL="$1"
    shift
fi

if [[ -n "$1" ]]; then
    MESSAGE="$*"
fi

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    TIMEZONE=$(date +%Z)
    HASH=$(echo -n "$MESSAGE" | sha256sum | awk '{print $1}')
    echo "[$TIMESTAMP $TIMEZONE] [$LOG_LEVEL] $HASH"
    sleep 5
done