#!/usr/bin/env bash

docker pull ibejohn818/stackformation:latest
docker run --rm -it \
    -v $(pwd):$(pwd) \
    -v $HOME/.aws:/root/.aws \
    -v $(pwd)/ansible:$(pwd)/ansible \
    -w $(pwd) \
    ibejohn818/stackformation:latest \
    stackformation "$@"
