## Log Output
### Usage
1. Start the cluster (uses medium compute resource)
`curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/gcloud_scripts/cluster_init.sh | bash`

2. Apply everything in one go
`curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/log_output/apply_all.sh | bash`

3. Run this to get response as an output text file
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/gcloud_scripts/make_requests_exercise.sh | bash -s -- 2>&1 | tee output
```
- OR get the address and inspect pages individually with `kubectl get gateway -n exercises`

4. Delete cluster once done
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/gcloud_scripts/delete_cluster.sh | bash
```