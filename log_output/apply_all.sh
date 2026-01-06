#!/bin/bash

curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash

# install istio operator for instio ingress gateway
kubectl create namespace istio-ingress
istioctl install -y -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: ingress
spec:
  profile: empty # Do not install CRDs or the control plane
  components:
    ingressGateways:
    - name: istio-ingressgateway
      namespace: istio-ingress
      enabled: true
      label:
        # Set a unique label for the gateway. This is required to ensure Gateways
        # can select this workload
        istio: ingressgateway
  values:
    gateways:
      istio-ingressgateway:
        # Enable gateway injection
        injectionTemplate: gateway
EOF

# Manifests for log-output
NS=exercises
kubectl create namespace $NS

echo "Manifests are applying..."
./kustomize build . | kubectl apply -f -
kubectl -n $NS rollout status deployment log-output-dep
kubectl -n $NS get services -o wide
kubectl -n $NS get ing

# cleanup kustomize binary... or not
rm kustomize

echo "All done!"