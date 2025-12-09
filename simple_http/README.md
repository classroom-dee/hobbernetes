## The Project
### 4.2 The project, step 21

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
- Create a Bucket named `simple-http-backups`
- Make an artifact registry named `test-repo`
- Init the cluster `./gcloud_scripts/cluster_init.sh`
- Push the tag and then push to main, wait for deployment success
- Edit the api manifest to have incorrect info and see it failing
- Correct the error and see it recovers
- Clean up the cluster `./gcloud_scripts/delete_cluster.sh` and the Artifact Registry