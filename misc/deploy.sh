#!/usr/bin/env bash

set -euo pipefail

pth="https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.3"

if [[ "${1:-}" == "--test" ]]; then
    echo "Ad-hoc"
    pth="/lab/dee/exercises/hobbernetes"
fi


rollout="${pth}/misc/manifests/rollout.yaml"
analysis="${pth}/misc/manifests/analysis-template.yaml"
argo_ns="argo-rollouts"

kubectl get ns $argo_ns >/dev/null 2>&1 || kubectl create ns $argo_ns

kubectl apply -f $rollout