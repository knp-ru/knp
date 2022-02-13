#!/usr/bin/env bash
docker run -d --rm --name=ddoser_normal --network=host \
        -v $PWD/normal.config.yaml:/usr/src/app/normal.config.yaml \
        -v $PWD/output:/usr/src/app/output \
        ahartanu/ddoser:1.2