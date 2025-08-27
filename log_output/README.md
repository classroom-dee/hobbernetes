## Log Output
### Usage
- Assuming you have your gcloud cli setup... AND you are on a UNIX based system
- You need git bash to run these if you are on Windows and run with `bash something.sh`
1. Start the cluster (I disabled logging and Prometheus because they kept giving OOM)
   - `./gcloud_scripts/cluster_init.sh`
2. Deploy pv and pvc
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/log_output/volumes/pvc.yaml`
3. Deploy configmap
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/log_output/volumes/configmap.yaml`
4. Deploy log output
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/log_output/manifests/deployment.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/log_output/manifests/service.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/log_output/manifests/ingress.yaml`
5. Deploy ping pong
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/ping_pong/manifests/secrets.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/ping_pong/manifests/statefulset.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/3.2/ping_pong/manifests/service.yaml`
6. Run this to get response as an output text file
   - `./gcloud_scripts/make_requests_exercise.sh > ./gcloud_scripts/output`
   - OR get the address and inspect pages individually
7. Delete cluster: `./gcloud_scripts/delete_cluster.sh`