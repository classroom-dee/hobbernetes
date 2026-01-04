#!/bin/bash

set -e

# services
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo-versions.yaml

# ingress gw
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/gateway-api/bookinfo-gateway.yaml

# no ingress needed
kubectl annotate gateway bookinfo-gateway networking.istio.io/service-type=ClusterIP --namespace=default

kubectl wait gateway bookinfo-gateway --for=condition=Programmed=True --timeout=120s

# kubectl port-forward svc/bookinfo-gateway-istio 8080:80
