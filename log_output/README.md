## Log Output 5.3
### Usage

1. Start the cluster & set kubeconfig `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.3/chapter6/service-mesh/start_k3d.sh)`

2. Install CLI: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.3/chapter6/service-mesh/install_istio.sh)`

3. Apply manifests: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.3/log_output/apply_all.sh)`

4. Monitoring
- `kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/addons/prometheus.yaml`
- `kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/addons/kiali.yaml`

5. Expose ingress `kubectl port-forward svc/istio-ingressgateway 8080:80 -n istio-ingress`

6. [Make requests](http://localhost:8080/logs/ping) sufficient times so the traffic diverges

7. Confirm traffic on Kiali `istioctl dashboard kiali`

### Note
- If you're on macOS, substitute the command for `eval $(curl -fsSL ...)`

### Questions
- All backends use the same principle for routing (rewrite svc-name/subpath -> lands on backend with subpath)
1. Why does the pingpong(Axum) backend need a separate subpathing?
2. If it was not the framework-specific problem, why did the istio sidecar not work the same way as for the other services? (adding double slashes for subpaths for pingpong, not for the other services)
3. Could the order of `kubectl apply` matter?
4. If it's not the istio problem, what then?