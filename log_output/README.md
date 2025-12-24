## Log Output 4.7
### Usage

1. Start the cluster, fork this repo and start ArgoCD, patch it to use LB, 
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.7/gcloud_scripts/cluster_init.sh | bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get secret -n argocd argocd-initial-admin-secret -o json
```

2. SA
- The assignment uses the Artifact Registry so unfortunately this step is relevant...
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
- other hard coded things : cluster name(`dwk-cluster`)

3. IAM
- The SA(the impersonated one) needs `roles/resourcemanager.projectIamAdmin` binding
- The compute SA that is automatically created on cluster setup needs at least `artifact registry reader` role

4. Github
- Check workflow permissions (RW)

5. On ArgoCD, add new app, set PATH to log_output, sync and see it progress.

6. make modifications, force push tag `4.7` with commit message `[log-output]`, and re-sync

7. Delete cluster once done
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.1/gcloud_scripts/delete_cluster.sh | bash
```