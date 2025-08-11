## The Project
- Let's a user add todos
- Saves a hero image in in-mem cache, refreshes periodically
- Periodically generates a  random todo and render it
- Collects request logs with Prom-Alloy stack and sends it to Loki, show it on Grafana

### Usage
1. Create ns: `kubectl create namespace project`
2. Make a mount path: `docker exec -it k3d-k3s-default-agent-0 mkdir /tmp/simple-http`
3. Deploy storage:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/volumes/pv.yaml`
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/volumes/pvc.yaml`
4. Deploy secret: Optionally encrypt-decrypt the secret
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/manifests/secrets.yaml`
5. Deploy Redis:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/manifests/redis.yaml`
6. Deploy manifest:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/manifests/statefulset.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/manifests/ingress.yaml`
7. Deploy cronjob: wait before the statefulset deploys completely
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/manifests/cronjob.yaml`
8. Deploy the monitoring stack
   - Note: Might have to change path to /var/log/containers in alloy_values2.yaml
   - `helm install prometheus-community/kube-prometheus-stack --generate-name --namespace prometheus`
   - `helm upgrade --install loki --namespace=loki-stack grafana/loki-stack --set loki.image.tag=2.9.3 --set grafana.enabled=false --set promtail.enabled=false`
   - `helm upgrade --install alloy grafana/k8s-monitoring -n loki-stack -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.10/simple_http/helm/alloy_values2.yaml`
   - Port forward grafana, setup loki data source to 'http://loki.loki-stack:3100'
8. Access it [here](http://localhost:8081) and add todos, a valid one and an invalid one
9. Check the Explore-logs section, make a query with a filter `app=simple-http`
10. Logs might spontaneously appear (todo generator)

### Memo
- Encrypt

```bash
age-keygen -o key.txt

sops --encrypt \
   --age <USE THE AGE PUBKEY OUTPUT> \
   --encrypted-regex '^(data)$' \
   secrets.yaml > secrets.enc.yaml
```

- Decrypt

```bash
export SOPS_AGE_KEY_FILE=$(pwd)/key.txt

sops --decrypt secrets.enc.yaml > secrets.yaml
```

or pipe directly 

```bash
sops --decrypt secrets.enc.yaml | kubectl apply -f -
```