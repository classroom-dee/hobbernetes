## The Project
- Let's a user add todos
- Saves a hero image in in-mem cache, refreshes periodically
- Periodically generates a  random todo and render it
- Collects request logs with Prom-Alloy stack and sends it to Loki, show it on Grafana

### Notes
- e2-small was used for monitoring stacks (previously e2-micro)

### Usage (for 3.8)
1. Create SA and key, add secrets to github env secrets
2. Check the workflow: `.github/workflow/main.yaml`
3. Init a cluster and create namespace `project-test-branch`
4. Create a test branch `git checkout -b test-branch`
5. Test the workflow: `git push origin --delete test-branch`
6. Confirm if the namespace is deleted on Lens or kubectl

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