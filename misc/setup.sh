#!/usr/bin/env bash


argo_ns="argo-rollouts"
kubectl create namespace $argo_ns
kubectl apply -n $argo_ns -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# prom setup
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prom prometheus-community/kube-prometheus-stack -n prometheus --create-namespace

service=$(
  kubectl get svc prom-kube-prometheus-stack-prometheus \
  -n prometheus \
  -o jsonpath='{.metadata.name}.{.metadata.namespace}.svc.cluster.local'
)
# kubectl -n prometheus port-forward "$prom_pod" 9090:9090

# argo rollout plugin setup
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts