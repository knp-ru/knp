#!/usr/bin/env bash
docker run -d --rm -p "8080:8080" -it --name=dumper daime/http-dump