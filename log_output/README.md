## Log Output
### Usage
- Assuming you have your gcloud cli setup... AND you are on a UNIX based system
- You need git bash to run these if you are on Windows and run with `bash something.sh`
- Gateway API init is included in the bash script

1. Start the cluster (I disabled logging and Prometheus because they kept giving OOM)
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/3.3/gcloud_scripts/cluster_init.sh | bash
```

2. Apply everything in one go
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/3.3/log_output/apply_all.sh | bash
```

3. Run this to get response as an output text file
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/3.3/gcloud_scripts/make_requests_exercise.sh | bash > output
```
- OR get the address and inspect pages individually with `kubectl get ing -n exercises`

4. Delete cluster once done
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/3.3/gcloud_scripts/delete_cluster.sh | bash
```