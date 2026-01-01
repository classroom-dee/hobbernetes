## Custom Resources: 5.1

### Note
- Used Rust because it was the smaller drop in my bucket 😉😛🤷

### Usage
1. Start the cluster: `curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/gcloud_scripts/cluster_init.sh | bash`
2. Apply manifests: `curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/chapter6/diy-crd/apply_all.sh | bash`
3. Check pod name `kubectl get po` and then port forward `kubectl port-forward copy-paster-..... 3000:3000`
4. [Result](http://localhost:3000)
5. Clean up: `curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.1/gcloud_scripts/delete_cluster.sh | bash`