#!/bin/bash

NS=wiki-replicator
kubectl create namespace $NS

# Enable injection
kubectl label namespace $NS istio-injection=enabled

# Manifests
echo "Manifests are applying..."
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/wiki-copy/stset.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/wiki-copy/svc.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/wiki-copy/gtw.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/wiki-copy/service-entry.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/wiki-copy/route.yaml
kubectl -n $NS rollout status statefulset wiki-replicator-sts

echo "All done!"