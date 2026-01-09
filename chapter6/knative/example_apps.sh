#!/bin/bash

# hello world app
./kn service create hello \
  --image ghcr.io/knative/helloworld-go:latest \
  --port 8080 \
  --env TARGET=World

# autoscaling: add -w for watching
kubectl get pod -l serving.knative.dev/service=hello

# make request
curl $(kubectl get ksvc -o jsonpath='{.items[0].status.url}')

# see the scaled up pods
kubectl get pod -l serving.knative.dev/service=hello

# see the pods downscale
echo "Waiting 2 minutes for pods to downscale..."
sleep 2m
kubectl get pod -l serving.knative.dev/service=hello

# making revision to hello
./kn service update hello --env TARGET=Knative

# make request
curl $(kubectl get ksvc -o jsonpath='{.items[0].status.url}')

# check revisions: default is 100% to the last revision
./kn revisions list

# split the traffic
kn service update hello \
  --traffic hello-00001=50 \
  --traffic @latest=50