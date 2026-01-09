#!/bin/bash

# Install CLIss
curl -Lo kn https://github.com/knative/client/releases/download/knative-v1.20.0/kn-linux-amd64 \
  && chmod +x ./kn \
  && curl -Lo kn-operator https://github.com/knative-extensions/kn-plugin-operator/releases/download/knative-v1.7.1/kn-operator-linux-amd64 \
  && chmod +x ./kn-operator \
  && mkdir -p ~/.config/kn/plugins \
  && mv kn-operator ~/.config/kn/plugins

# Install CRDs
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.1/serving-crds.yaml

# Core components
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.1/serving-core.yaml

# Install Kourier controller
kubectl apply -f https://github.com/knative-extensions/net-kourier/releases/download/knative-v1.20.0/kourier.yaml

# Patch kn to use Kourier
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'

# Get external address
kubectl --namespace kourier-system get service kourier

# Magic DNS
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.1/serving-default-domain.yaml

# Set the correct versions for pods
kubectl version | grep Server # *check your k3s version*
kubectl set env -n knative-serving deployment/controller KUBERNETES_MIN_VERSION=1.31.5+k3s1
kubectl set env -n knative-serving deployment/net-kourier-controller KUBERNETES_MIN_VERSION=1.31.5+k3s1
kubectl set env -n knative-serving deployment/webhook KUBERNETES_MIN_VERSION=1.31.5+k3s1
kubectl set env -n knative-serving deployment/activator KUBERNETES_MIN_VERSION=1.31.5+k3s1
kubectl set env -n knative-serving deployment/autoscaler KUBERNETES_MIN_VERSION=1.31.5+k3s1

# Not needed
# Patch it to be reachable from outside the cluster
# kubectl patch configmap/config-domain \
#       --namespace knative-serving \
#       --type merge \
#       --patch '{"data":{"example.com":""}}'

# kubectl get ksvc