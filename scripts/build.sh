#!/bin/bash
commit_hash=$(git log -n1 --format=format:%H)
tag=registry.harrisonkiang.com/container-registry/admission-webhooks:$commit_hash
echo Building and pushing $tag
docker build -t $tag .
docker push $tag
