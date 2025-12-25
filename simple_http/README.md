## The Project 4.9
### What
- Deploys to release, if tag-based push otherwise, to main

### Usage
1. Start the cluster, fork this repo and start ArgoCD, patch it to use LB, install prom and NATS
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.9/gcloud_scripts/cluster_init.sh | bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get secret -n argocd argocd-initial-admin-secret -o json
helm install prom prometheus-community/kube-prometheus-stack -n prometheus --create-namespace
helm install \
  my-nats oci://registry-1.docker.io/bitnamicharts/nats \
  --set image.registry=docker.io \
  --set image.repository=bitnamilegacy/nats \
  --set image.tag=2.11.8-debian-12-r0 \
  --set metrics.enabled=true \
  --set auth.enabled=false \
  --set metrics.image.registry=docker.io \
  --set metrics.image.repository=bitnamilegacy/nats-exporter \
  --set metrics.image.tag=0.17.3-debian-12-r8 \
  --set metrics.serviceMonitor.enabled=true \
  --set metrics.serviceMonitor.namespace=prometheus
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

5. On ArgoCD, add new app, set PATH to either `simple_http/overlays/prod/kustomization.yaml` or `.../staging/kustomization.yaml`, namespace to `project-4-9-prod` or if staging, `project-stage`, sync and see it progress.

6. make modifications, force push tag `4.9` with commit message `[simple-http]`, and re-sync, if there was a previous run, delete the pod to refresh.

7. NATS feeds are printed in the pod log 

8. Delete cluster once done
```bash
curl -fsSL https://raw.githubusercontent.com/boolYikes/hobbernetes/4.9/gcloud_scripts/delete_cluster.sh | bash
```