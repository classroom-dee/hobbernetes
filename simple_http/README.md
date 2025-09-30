## The Project
- Let's a user add todos
- Saves a hero image in in-mem cache, refreshes periodically
- Periodically generates a  random todo and render it
- Collects request logs with Prom-Alloy stack and sends it to Loki, show it on Grafana

### Notes
- e2-small was used for monitoring stacks (previously e2-micro)

### Usage
1. Create a docker repository `test-repo` in the GCP artifact registry, cleanup policy: most recent, disable scanning
2. Create SA and key, add secrets to github env secrets
3. Check the workflow: `.github/workflow/main.yaml`
4. Checkout to the test branch `git checkout test-branch`, make changes, commit and push
5. Wait for GA to complete
6. Get the address `kubectl get ing -n project`
7. Test it: `http://<adderss>` -> add random page every 1hr
8. **Below are not tested with this release. (I wasn't sure if monitoring was within the scope)**
9. ~~Deploy the monitoring stack~~
   - Note: Might have to change path to /var/log/containers in alloy_values2.yaml
   - `helm install prometheus-community/kube-prometheus-stack --generate-name --namespace prometheus`
   - `helm upgrade --install loki --namespace=loki-stack grafana/loki-stack --set loki.image.tag=2.9.3 --set grafana.enabled=false --set promtail.enabled=false`
   - `helm upgrade --install alloy grafana/k8s-monitoring -n loki-stack -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.5/simple_http/helm/alloy_values2.yaml`
   - Port forward grafana, setup loki data source to 'http://loki.loki-stack:3100'
10. ~~Access it [here](http://localhost:8081) and add todos, a valid one and an invalid one~~
11. ~~Check the Explore-logs section, make a query with a filter `app=simple-http`~~
12. ~~Logs might spontaneously appear (todo generator)~~
13. **Clean up the Artifact Registry**

### Memo
- Don't use `echo ""` (it adds new lines), use `printf "" | base64`
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