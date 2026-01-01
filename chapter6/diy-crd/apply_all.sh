#!/bin/bash

echo "Manifests are applying..."

kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/manifests/sa.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/manifests/role.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/manifests/rolebinding.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/manifests/dummysite-crd-def.yaml
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/manifests/controller.yaml

kubectl wait --for=condition=Established crd/dummysites.stable.dwk --timeout=60s
kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/manifests/dummysite.yaml

echo "All done!"