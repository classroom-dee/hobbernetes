#!/bin/bash

# secrets, pg stset and the service
kubectl create namespace exercises
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/ping_pong/manifests/secrets.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/ping_pong/manifests/statefulset.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/ping_pong/manifests/service.yaml

## Pingpong serverless!
## "PORT" is reserved
# ./kn service create -n exercises ping-pong \
#   --image xuanminator/ping-pong:5.7 \
#   --port 8080 \
#   --env PINGPONG_PORT="8080"
## OR
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/ping_pong/manifests/pingpong-knative-serverless.yaml



# autoscaling: add -w for watching
kubectl get pod -l serving.knative.dev/service=ping-pong -n exercises

# make request
curl $(kubectl get ksvc -o jsonpath='{.items[0].status.url}' -n exercises)

# see the scaled up pods
kubectl get pod -l serving.knative.dev/service=ping-pong -n exercises

# see the pods downscale
echo "Waiting 2 minutes for pods to downscale..."
sleep 2m
kubectl get pod -l serving.knative.dev/service=ping-pong -n exercises

# making revision to the image
./kn service update ping-pong --env PINGPONG_VERSION=V2 -n exercises

# make request
curl $(kubectl get ksvc -o jsonpath='{.items[0].status.url}' -n exercises)

# check revisions: default is 100% to the last revision
./kn revisions list -n exercises

# split the traffic
./kn service update ping-pong -n exercises \
  --traffic ping-pong-00002=50 \
  --traffic @latest=50