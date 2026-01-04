#!/bin/bash

set -e


CLUSTER_NAME="k3s-default"
CONFIG_NAME="k3d-k3s-default"

# coalesce cluster start/creation
k3d cluster list | grep -q "^$CLUSTER_NAME\b" && k3d cluster start $CLUSTER_NAME || \
  k3d cluster create --api-port 6550 -p '9080:80@loadbalancer' -p '9443:443@loadbalancer' --agents 2 --k3s-arg '--disable=traefik@server:*' $CLUSTER_NAME

# k3d kubeconfig get $CLUSTER_NAME
 --skip-confirmation
config_path=$(k3d kubeconfig merge "$CLUSTER_NAME")

# Maybe only one of these is needed but I'm not sure
export KUBECONFIG="$config_path"
kubectl --kubeconfig "$config_path" config use-context "$CONFIG_NAME"

kubectl get nodes