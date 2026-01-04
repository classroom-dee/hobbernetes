#!/bin/bash

set -e

# labeling does all the heavy lifting
kubectl label namespace default istio.io/dataplane-mode=ambient

# prom
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/addons/prometheus.yaml

# kiali
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/addons/kiali.yaml

# access dashboard
# istioctl dashboard kiali

# send payload (portforward beforehand)
# for i in $(seq 1 100); do curl -sSI -o /dev/null http://localhost:8080/productpage; done

