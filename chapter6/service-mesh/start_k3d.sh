#!/bin/bash


CLUSTER_NAME="k3s-default"
CONFIG_NAME="k3d-k3s-default"

# coalesce cluster start/creation
k3d cluster list | \
  grep -q "^$CLUSTER_NAME\b" && \
  k3d cluster start $CLUSTER_NAME || \
  k3d cluster create -p 8082:30080@agent:0 -p 8081:80@loadbalancer \
    --agents 2 --k3s-arg "--disable=traefik@server:0" $CLUSTER_NAME

# k3d kubeconfig get $CLUSTER_NAME
config_path=$(k3d kubeconfig merge "$CLUSTER_NAME")

# Maybe only one of these is needed but I'm not sure
export KUBECONFIG="$config_path"
kubectl --kubeconfig "$config_path" config use-context "$CONFIG_NAME"