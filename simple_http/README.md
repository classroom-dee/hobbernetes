## The Project
### 3.12.1 Intermission?

1. SA
- No longer using JSON SA key -> 
- need to setup a workload federation with attributes. I set the condition to check `owner/repo`
- and then bind the principal to an SA (impersonation) with `Workload Identity User` role
- These vars must be present in github secrets
- GKE_PROJECT -> project id
- GKE_PROJECT_NAME
- GKE_PROJECT_NUMBER
- GSA_ID -> the front part of the SA email
- other hard coded things : cluster name(dwk-cluster), bucket name(mooc-sdw), bucket subfolder(db-backups)

2. IAM
- The SA needs `roles/resourcemanager.projectIamAdmin` binding
- The compute SA that is created on cluster setup needs at least `artifact registry reader` role


3. The Rest
- Follow instructions on [3.11](https://github.com/classroom-dee/hobbernetes/tree/3.11/simple_http)
- Go to the observation deck! [metrics explorer](https://console.cloud.google.com/monitoring/metrics-explorer)
- Select metrics -> Prometheus target -> Query "Todo" -> select .../count
![alt text](image-1.png)