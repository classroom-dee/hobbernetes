## Log Output
### Usage
1. Start the cluster (uses medium compute resource)
```
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/gcloud_scripts/cluster_init.sh | bash
```

2. Apply everything in one go
```
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/log_output/apply_all.sh | bash
```

3. Get the address (takes some time to warm up)
```
kubectl get gateway log-output-gateway -n exercises -o jsonpath='{.status.addresses[*].value}'
```

4. Kill the postgres container and check readiness (It will go from 2/2, 2/2 to 2/2, 1/2 for log_output and pingpong respectively and then restart after a moment)
```
kubectl exec -n exercises -it ping-pong-stset-0 --container=postgres -- kill 1

kubectl get pods -n exercises
```

5. Delete cluster once done
```
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/gcloud_scripts/delete_cluster.sh | bash
```