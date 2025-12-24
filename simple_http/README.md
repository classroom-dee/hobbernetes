## The Project 4.8
### Usage

1. Start the cluster, fork this repo and start ArgoCD, patch it to use LB, 
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.8/gcloud_scripts/cluster_init.sh | bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get secret -n argocd argocd-initial-admin-secret -o json
```

2. SA
- Setup a workload federation attributes
  - id: github-actions-pool
  - provider type: OIDC, github provider
  - issuer: `https://token.actions.githubusercontent.com`
  - audience: insert proj number -> `https://iam.googleapis.com/projects/<project number>/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider`
  - attrib mapping: `attribute.repository` --> `assertion.repository`
  - attrib conditions: `attribute.repository == "<your username>/hobbernetes"`
- Insert project number -> `principal://iam.googleapis.com/projects/<project number>/locations/global/workloadIdentityPools/github-actions-pool/subject/SUBJECT_ATTRIBUTE_VALUE`
- Bind the above fed principal to your SA (impersonation) with `Workload Identity User` role
- These vars must be present in github secrets
- `GKE_PROJECT` -> project id
- `GKE_PROJECT_NAME`
- `GKE_PROJECT_NUMBER`
- `GSA_ID` -> the front part of the SA email
- `DISCORD_HOOK_URL`
- other hard coded things : cluster name(`dwk-cluster`), bucket name(`mooc-sdw`), bucket subdir(`db-backups`)

3. IAM
- The SA(the impersonated one) needs `roles/resourcemanager.projectIamAdmin` binding
- The compute SA that is automatically created on cluster setup needs at least `artifact registry reader` role

4. Github
- Check workflow permissions (RW)

5. On ArgoCD, add new app, set PATH to simple_http, namespace to `project-4-8`, sync and see it progress.

6. make modifications, force push tag `4.8` with commit message `[simple-http]`, and re-sync

7. Delete cluster once done
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.8/gcloud_scripts/delete_cluster.sh | bash
```