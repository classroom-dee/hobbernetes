## The Project
- Let's user add todos
- Saves a hero image in in-mem cache, refreshes periodically
- Periodically generates a  random todo and render it

### Usage
1. Create ns: `kubectl create namespace project`
2. Make a mount path: `docker exec -it k3d-k3s-default-agent-0 mkdir /tmp/simple-http`
3. Deploy storage:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/volumes/pv.yaml`
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/volumes/pvc.yaml`
4. Deploy secret: Optionally encrypt-decrypt the secret
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/manifests/secrets.yaml`
5. Deploy Redis:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/manifests/redis.yaml`
6. Deploy manifest:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/manifests/statefulset.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/manifests/ingress.yaml`
7. Deploy cronjob: wait before the statefulset deploys completely
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.9/simple_http/manifests/cronjob.yaml`
8. Access it [here](http://localhost:8081)
9. Websocket-refresh check: use `curl -X POST http://localhost:8081/todos -H "Content-Type: application/json" -d '{"item": "something"}'` and then check browser

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