#!/bin/bash

### L4 Enforcement
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
EOF

# different SA access test
# kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/curl/curl.yaml
# kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage" # see it fail


### L7 Enforcement
# waypoint proxy needed
istioctl waypoint apply --enroll-namespace --wait
# kubectl get gtw waypoint # check if up and running
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-waypoint
  namespace: default
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/curl
    to:
    - operation:
        methods: ["GET"]
EOF

# and allow waypoint from L4
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
        - cluster.local/ns/default/sa/waypoint
EOF

# tests
kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage" -X DELETE # fails
kubectl exec deploy/reviews-v1 -- curl -s http://productpage:9080/productpage # fails
kubectl exec deploy/curl -- curl -s http://productpage:9080/productpage | grep -o "<title>.*</title>" # succeeds