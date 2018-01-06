#!/usr/bin/env bash
docker pull ibejohn818/stackformation:latest
docker run --rm -it \
    -v $(pwd):$(pwd) \
    -v $HOME/.aws:$HOME/.aws \
    -v /etc/passwd:/etc/passwd \
    -v $(pwd)/ansible:$(pwd)/ansible \
    -w $(pwd) \
    -u $(id -u):$(id -g) \
    ibejohn818/stackformation:latest \
    stackformation "$@"
