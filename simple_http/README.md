## The Project
### 4.4 The project, step 22

**Hope you don't find the procedure too tedious! Maybe i shouldn't have used workflow in this exercise?**

1. SA
- No longer using JSON SA key (accidentally moved the gcp project under an org -> no permission to enable json key 🤷🏾) -> 
- need to setup a workload federation with attributes `attribute.repository = assertion.repository etc etc...`. I set the condition to check `owner/repo`
- and then bind the principal to an SA (impersonation) with `Workload Identity User` role
- These vars must be present in github secrets
- `GKE_PROJECT` -> project id
- `GKE_PROJECT_NAME`
- `GKE_PROJECT_NUMBER`
- `GSA_ID` -> the front part of the SA email
- other hard coded things : cluster name(`dwk-cluster`), bucket name(`mooc-sdw`), bucket subfolder(`db-backups`)

2. IAM
- The SA(the impersonated one) needs `roles/resourcemanager.projectIamAdmin` binding
- The compute SA that is automatically created on cluster setup needs at least `artifact registry reader` role
- Add permission `storage object admin` (although I think storage object creator is enough)

3. The Rest
- Edit/check workflow .github/workflow/main.yaml for secret names
- Create a Bucket named `mooc-sdw` and a subdir `db-backups`
- Make an artifact registry named `test-repo`
- Init the cluster `./gcloud_scripts/cluster_init.sh`
- Push the tag and then push to main, wait for deployment success
- `kubectl get ing -n project` to get the address
- Test adding/ticking it off as done
- Clean up the cluster `./gcloud_scripts/delete_cluster.sh` and the Artifact Registry