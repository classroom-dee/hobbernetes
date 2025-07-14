## Log Output
### Usage
1. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.11/log_output/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.11/log_output/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/1.11/log_output/manifests/ingress.yaml`
2. The periodical logs can be accessed with [here](http://localhost:8081/logs/all)
3. The ping count + hashed log can be accessed [here](http://localhost:8081/logs/ping)
4. : Paths other than /logs gives you 404