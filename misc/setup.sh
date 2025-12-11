#!/usr/bin/env bash


argo_ns="argo-rollouts"
kubectl apply -n $argo_ns -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prom prometheus-community/kube-prometheus-stack -n prometheus --create-namespace


prom_pod=$(kubectl -n prometheus get pod -l app.kubernetes.io/name=prometheus -o jsonpath="{.items[0].metadata.name}")
kubectl -n prometheus port-forward "$prom_pod" 9090:9090