## Ping Pong
### Usage
1. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.11/ping_pong/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.11/ping_pong/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.11/ping_pong/manifests/ingress.yaml`
2. [Make request here](http://localhost:8081/pingpong) to increase ping count