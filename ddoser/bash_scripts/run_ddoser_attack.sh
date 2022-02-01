#!/usr/bin/env bash
docker run -d --rm --name=ddoser_attack --network=host \
        -v $PWD/attack.config.yaml:/usr/src/app/attack.config.yaml \
        -v $PWD/output:/usr/src/app/output \
        ahartanu/ddoser:1.2 attack.config.yaml