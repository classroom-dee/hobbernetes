## The Project
### 3.11. Scaling
- Create SA and key, add secrets to github env secrets
- Add SA permission `storage object admin` (although I think `storage object creator` is enough)
- Add SA key.json to github secrets. One as-is, one as base64 (double-quote issue): `GKE_SA_KEY`, `GKE_SA_KEY_B64`
- Edit/check workflow `.github/workflow/main.yaml` for secret names
- Create a Bucket named `simple-http-backups`
- Init the cluster `gcloud_scripts/cluster_init.sh`
- Meanwhile make an artifact registry named `test-repo`
- Create namespace `project`
- `git push`
- Get the address using `kubectl get svc -n project`
- Make a lot of requests to `/todo` (maybe with a loop in a bash script)
- Limits and requests are set low intentionally for replication
- Clean up the cluster `gcloud_scripts/delete_cluster.sh` and the Artifact Registry