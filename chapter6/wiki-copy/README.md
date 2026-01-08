## 5.4 Wikipedia with init and sidecar

### Usage
1. Start k3d `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/service-mesh/start_k3d.sh)`
  
2. Install CLI: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/service-mesh/install_istio.sh)`

3. Apply all: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.4/chapter6/wiki-copy/apply_all.sh)`

4. Expose the gateway
- `kubectl get po -n wiki-replicator` check the gateway pod
- `kubectl -n wiki-replicator port-forward <gateway pod here> 8080:80 --address 0.0.0.0`
- [Visit the mirror](http://localhost:8080). Fast forward **n** minutes, the results diverge between two replicas

### Bugs
- Sometimes get empty pages with a lone title header

### Note
- If the sidecar spec (spec.restartPolicy) won't validate, move it under the regular container spec without the restartPolicy.
- Apparently putting it under regular container is more universal but we're trying out things 😛
- Check istio-proxy `kubectl -n wiki-replicator get pod wiki-replicator-sts-0 -o jsonpath='{.spec.containers[*].name}'`
- Can't egress before Envoy is ready and init container might start before Envoy -> mesh exclusion
- Might as well have done it with the default ingress + LB 🤮
- Replicas without route traffic ratio -> round robin?