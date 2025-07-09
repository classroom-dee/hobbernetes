## Log Output
### Usage
1. Note: Application port is in the deployment manifest file
2. Deploy 
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.8/simple_http/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.8/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.8/simple_http/manifests/ingress.yaml`
3. Access via `http://localhost:8081`