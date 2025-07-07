## Log Output
### Usage
1. Port section is in the manifest file
2. Deploy with `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.5/simple_http/manifests/deployment.yaml`
3. Open proxy with `kubectl port-forward deployment/simple-http 8060:8060`
4. Make request from client: `curl http://localhost:8060`