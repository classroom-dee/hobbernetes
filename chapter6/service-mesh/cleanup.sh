#!/bin/bash

# waypoint proxies
kubectl label namespace default istio.io/use-waypoint-
istioctl waypoint delete --all

# ambient data plane removal from the ns
kubectl label namespace default istio.io/dataplane-mode-

# book app and curl app
kubectl delete httproute reviews
kubectl delete authorizationpolicy productpage-viewer
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/curl/curl.yaml
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo.yaml
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo-versions.yaml
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/gateway-api/bookinfo-gateway.yaml

# istio client and controller
istioctl uninstall -y --purge
kubectl delete namespace istio-system

# gateway api crd
kubectl delete -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml

# cluster shutdown
k3d cluster stop