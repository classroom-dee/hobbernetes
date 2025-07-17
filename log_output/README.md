## Log Output
### Usage
1. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/ping_pong/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/ping_pong/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/log_output/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/log_output/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/log_output/manifests/ingress.yaml`
2. Volumes(Optional: not used in this exercise but for safety)
   - `docker exec -it k3d-k3s-default-agent0 mkdir /tmp/kube`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/log_output/volumes/pv.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.1/log_output/volumes/pvc.yaml`
3. Make a number of requests to /pingpong [here](http://localhost:8081/pingpong)
4. The ping count + hashed log can be accessed [here](http://localhost:8081/logs/ping)
5. The root / was avoided because it is used by simple-http (trying to make it coexist)