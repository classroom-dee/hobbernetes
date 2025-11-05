## The Project
### 3.10. Redundancy
- Create SA and key, add secrets to github env secrets
- Add SA permission `storage object admin` (although I think `storage object creator` is enough)
- Add SA key.json to github secrets. One as-is, one as base64 (double-quote issue): `GKE_SA_KEY`, `GKE_SA_KEY_B64`
- Edit/check workflow `.github/workflow/main.yaml` for secret names
- Create a Bucket named `simple-http-backups`
- Init the cluster `gcloud_scripts/cluster_init.sh`
- Create namespace `project`
- `git push`
- If build succeeds, run an ad-hoc job `kubectl -n project create job --from=cronjob/simple-http-backup adhoc-job`
- Check the job `kubectl -n project get job` and then check the GCS Bucket
- Clean up the cluster `gcloud_scripts/delete_cluster.sh` and the artifact registry