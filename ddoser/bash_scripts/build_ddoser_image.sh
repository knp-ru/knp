#!/bin/bash
# Run from ddoser path

if [[ "${PWD##*/}" != "ddoser" ]]; then
    echo "Run from ddoser path"
    exit 1
fi

docker build -t ahartanu/ddoser:1.2 .