#!/usr/bin/env bash

if [ "$1" = 'api' ]; then
    python3 src/app.py
    exec echo 'api'
else
    exec "$@"
fi