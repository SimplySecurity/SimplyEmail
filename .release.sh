#!/usr/bin/env bash
set -ex
# Requires the following packages: git, hub, docker
# SET THE FOLLOWING VARIABLES
USERNAME=simplysecurity
IMAGE=simplyemail
VERSION="$(cat VERSION)"

# UPDATE THE SOURCE CODE
git pull

# bump version
docker run --rm -v "$PWD":/app treeder/bump patch
VERSION=`cat VERSION`
echo "version: $VERSION"

# TAF, PULL, MERGE DEV
git checkout -b "dev"
git add --all
git commit -m "SimplyEmail $VERSION Release"
git tag -a "$VERSION" -m "SimplyEmail $VERSION Release"
git push origin "dev"
git push origin "dev" --tags
git checkout master
git merge "dev"
git push
hub release create dev -m  "SimplyEmail $VERSION Release"

# ALERT VERSION
echo "Building Version: $VERSION"

# START BUILD
./.build.sh

# DOCKER TAG/VERSIONING
docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$VERSION

# PUSH TO DOCKER HUB
docker push $USERNAME/$IMAGE:latest
echo "Docker image pushed: $USERNAME/$IMAGE:latest"
docker push $USERNAME/$IMAGE:$VERSION
echo "Docker image pushed: $USERNAME/$IMAGE:$VERSION"
