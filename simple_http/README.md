## The Project
### 4.6 The project, step 23

**Hope you don't find the procedure too tedious! Maybe i shouldn't have used workflow in this exercise?**

1. SA
- No longer using JSON SA key (accidentally moved the gcp project under an org -> no permission to enable json key 🤷🏾) -> 
- need to setup a workload federation with attributes `attribute.repository = assertion.repository etc etc...`. I set the condition to check `owner/repo`
- and then bind the principal to an SA (impersonation) with `Workload Identity User` role
- These vars must be present in github secrets
- `DISCORD_HOOK_URL` -> fsopen webhook
- `GKE_PROJECT` -> project id
- `GKE_PROJECT_NAME`
- `GKE_PROJECT_NUMBER`
- `GSA_ID` -> the front part of the SA email
- other hard coded things : cluster name(`dwk-cluster`), bucket name(`mooc-sdw`), bucket subfolder(`db-backups`)

2. IAM
- The SA(the impersonated one) needs `roles/resourcemanager.projectIamAdmin` binding
- The compute SA that is automatically created on cluster setup needs at least `artifact registry reader` role
- Add permission `storage object admin` (although I think storage object creator is enough)

3. GCS
- Create a Bucket named `mooc-sdw` and a subdir `db-backups`
- Make an artifact registry named `test-repo`

4. Init the cluster: `./gcloud_scripts/cluster_init.sh`

5. Messanger & Prom setup
- I separated NATS and Prom from the workflow (...not part of the app so it felt semantically correct)
- Please refer to the [Notes](#notes) below

6. The Rest
- Edit/check workflow .github/workflow/main.yaml for any missing secret vars
- Push the tag and then push to main, wait for deployment success
- `kubectl get ing -n project` to get the address
- Test adding/ticking it off as done
- Check the discord webhook channel
- Clean up the cluster `./gcloud_scripts/delete_cluster.sh` and the Artifact Registry


### Notes
1. Prometheus
`helm install prom prometheus-community/kube-prometheus-stack -n prometheus --create-namespace`

2. NATS
- Uses legacy repo
```bash
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

3. Attaching labels
- `kubectl get prometheus -n prometheus` -> find name e.g., `prom-kube-prometheus-stack-prometheus`
- `kubectl describe prometheus -n prometheus prom-kube-prometheus-stack-prometheus` -> look for: Service Monitor Selector::Match Labels::Release e.g., `prom`
- `kubectl label servicemonitors.monitoring.coreos.com -n prometheus my-nats-metrics release=prom`
