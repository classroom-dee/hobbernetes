## Log Output
### Usage
1. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.10/log_output/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.10/log_output/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.10/log_output/manifests/ingress.yaml`
2. Access it [here](http://localhost:8081/logs): Paths other than /logs gives you 404