#!/bin/bash

curl -L https://istio.io/downloadIstio | sh -
cd istio-1.28.2
export PATH=$PWD/bin:$PATH

istioctl version

istioctl install --set profile=ambient --set values.global.platform=k3d --skip-confirmation

kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null \
 || kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml