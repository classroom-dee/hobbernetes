## Ping Pong
### Usage
1. Shared ingress from log_output
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.1/log_output/manifests/ingress.yaml`
2. Secrets
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.1/ping_pong/manifests/secrets.yaml`
3. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.1/ping_pong/manifests/statefulset.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.1/ping_pong/manifests/service.yaml`
4. Get the external ip
   - `kubectl get svc ping-pong-svc -n exercises --output=jsonpath='{.status.loadBalancer.ingress[0].ip}'`
4. Copy the ip and use `http://(external_ip)/pingpong` to make requests