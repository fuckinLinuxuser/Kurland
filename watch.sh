#!/usr/bin/env bash
while inotifywait -r -e modify,create,delete ./frontend; do
    docker exec nginx nginx -s reload
done
