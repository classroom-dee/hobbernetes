#!/bin/bash

echo "Manifests are applying..."
kubectl create namespace exercises
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/log_output/volumes/pvc.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/log_output/volumes/configmap.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/log_output/manifests/deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/log_output/manifests/service.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/ping_pong/manifests/secrets.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/ping_pong/manifests/statefulset.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/ping_pong/manifests/service.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/log_output/manifests/gateway.yaml
kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.4/log_output/manifests/httproute.yaml

echo "All done!"