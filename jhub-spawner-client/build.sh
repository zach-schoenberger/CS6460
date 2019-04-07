#!/bin/bash
docker build -f ./jhub.Dockerfile -t zschoenb/jhub-notebook:latest . && docker push zschoenb/jhub-notebook:latest