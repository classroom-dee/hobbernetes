## Log Output
### Usage
1. Deploy pv and pvc:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/log_output/volumes/pv.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/log_output/volumes/pvc.yaml`
2. Deploy configmap:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/log_output/volumes/configmap.yaml`
2. Deploy ping pong
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/ping_pong/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/ping_pong/manifests/service.yaml`
3. [Make request here](http://localhost:8081/pingpong) to increase ping count
4. Deploy log output
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/log_output/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/log_output/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.5/log_output/manifests/ingress.yaml`
5. All logs are served [here](http://localhost:8081/logs/all), the ping message is served [here](http://localhost:8081/logs/ping)