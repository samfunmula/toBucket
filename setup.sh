#!/bin/bash

DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
source "$DIR/.env"
docker build --tag "$DOCKER_REPOSITORY/$DOCKER_PROJECT/$DOCKER_IMAGE:$DOCKER_TAG" .
docker push "$DOCKER_REPOSITORY/$DOCKER_PROJECT/$DOCKER_IMAGE:$DOCKER_TAG"