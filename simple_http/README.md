## The Project
aka 'simple http'
### Usage
1. Create ns: `kubectl create namespace project`
2. Make a mount path: `docker exec -it k3d-k3s-default-agent-0 mkdir /tmp/simple-http`
3. Deploy storage:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.4/simple_http/volumes/pv.yaml`
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.4/simple_http/volumes/pvc.yaml`
4. Deploy manifest:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.4/simple_http/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.4/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.4/simple_http/manifests/ingress.yaml`
5. Access it [here](http://localhost:8081)