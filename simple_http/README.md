## The Project
aka 'simple http'
### Usage
1. Create ns: `kubectl create namespace project`
2. Make a mount path: `docker exec -it k3d-k3s-default-agent-0 mkdir /tmp/simple-http`
3. Deploy storage:
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.8/simple_http/volumes/pv.yaml`
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.8/simple_http/volumes/pvc.yaml`
4. Deploy secret: Optionally encrypt-decrypt the secret
   - `https://raw.githubusercontent.com/boolYikes/hobbernetes/2.8/simple_http/manifests/secrets.yaml`
5. Deploy manifest:
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.8/simple_http/manifests/statefulset.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.8/simple_http/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.8/simple_http/manifests/ingress.yaml`
6. Access it [here](http://localhost:8081)

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