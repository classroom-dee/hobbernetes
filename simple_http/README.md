## Log Output
### Usage
1. Note: Application port is in the deployment manifest file
2. Make a mount path: `docker exec -it k3d-k3s-default-agent-0 mkdir /tmp/simple-http`
3. Deploy pv:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/1.12/simple_http/volumes/pv.yaml`
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/1.12/simple_http/volumes/pvc.yaml`
4. Deploy manifest:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.12/simple_http/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.12/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.12/simple_http/manifests/ingress.yaml`
5. Access via `http://localhost:8081/100` or use other uri like /500, /400 ... *The suggested uri 1200 does not work*