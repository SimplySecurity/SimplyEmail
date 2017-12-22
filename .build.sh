
#!/usr/bin/env bash
set -ex
# SET THE FOLLOWING VARIABLES
# docker hub username
USERNAME=simplysecurity
# image name
IMAGE=simplyemail
# version
VERSION="$(cat VERSION)"

docker build -t $USERNAME/$IMAGE:latest .
