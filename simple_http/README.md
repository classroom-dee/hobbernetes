## Log Output
### Usage
1. Make a mount path: `docker exec -it k3d-k3s-default-agent-0 mkdir /tmp/simple-http`
2. Deploy pv: No change made
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.2/simple_http/volumes/pv.yaml`
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.2/simple_http/volumes/pvc.yaml`
3. Deploy manifest:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.2/simple_http/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.2/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.2/simple_http/manifests/ingress.yaml`
4. Access it [here](http://localhost:8081)