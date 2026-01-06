## Log Output 5.3
### Usage

1. 
1. Start the cluster & set kubeconfig `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.3/chapter6/service-mesh/start_k3d.sh)`

2. Install CLI: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.3/chapter6/service-mesh/install_istio.sh)`

3. Apply manifests: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.3/log_output/apply_all.sh)`

4. Port forward istio gtw svc, confirm on Kiali

### Note
- If you're on macOS, substitute the command for `eval $(curl -fsSL ...)`