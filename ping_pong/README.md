## Ping Pong
### Usage
1. [Follow these instructions](https://github.com/boolYikes/hobbernetes/tree/1.7/log_output) save for the ingress manifest
2. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.9/ping_pong/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.9/ping_pong/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.9/ping_pong/manifests/ingress.yaml`
3. Access it via `http://localhost:8081/pingpong`