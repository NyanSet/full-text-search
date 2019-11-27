#!/usr/bin/env sh

if [ "$1" = 'build-index' ]; then
    python3 src/build.py
    python3 src/app.py
    exec echo 'build'
elif [ "$1" = 'start-api' ]; then
    python3 src/app.py
    exec echo 'api'
else
    exec "$@"
fi