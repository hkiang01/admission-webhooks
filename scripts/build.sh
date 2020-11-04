#!/bin/bash

registry=registry.harrisonkiang.com/container-registry/admission-webhooks

commit tag based on current git commit hash
commit_hash=$(git log -n1 --format=format:%H)
tag=$registry:$commit_hash
echo Building and pushing $tag
docker build -t $tag .
docker push $tag

# update manifests
sed -i "s/registry\.harrisonkiang\.com\/container-registry\/admission-webhooks:.*/registry\.harrisonkiang.com\/container-registry\/admission-webhooks:$tag/g" ../kubernetes/deployment.yaml
