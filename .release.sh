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
git checkout -b "Version-$VERSION"
git add --all
git commit -m "SimplyEmail $VERSION Release"
#git tag -a "$VERSION" -m "SimplyEmail $VERSION Release"
git push origin "Version-$VERSION"
#git push origin "Version-$VERSION" --tags
git checkout master
git merge "Version-$VERSION"
git push
hub release create Version-$VERSION -m "SimplyEmail $VERSION Release"
# DEL BRANCH
#git branch -d "dev"
#git branch -D "dev"

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

# GENERATE CHANGELOG FOR TAG AND PUSH
github_changelog_generator
git add --all
git commit -m "Update CHANGLOG.md from version bump"
git push 

