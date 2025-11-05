## The Project
### 3.10. Redundancy
- Create SA and key, add secrets to github env secrets
- Add SA permission `storage object admin` (although I think `storage object creator` is enough)
- Check workflow `.github/workflow/main.yaml`
- Init the cluster `gcloud_scripts/cluster_init.sh`
- Create namespace `project`
- `git push`