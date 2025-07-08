## Log Output
### Usage
1. Port section is in the manifest file
2. Deploy with `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.6/simple_http/manifests/deployment.yaml`
3. Apply service: `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.6/simple_http/manifests/service.yaml`
4. Open `http://localhost:8082`with a browser