## Ping Pong
### 4.4 Your canary
1. Install argo rollout & prom
- `curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.4/misc/setup.sh | bash` 
2. Deploy manifests
- `kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.4/ping_pong/manifests/secrets.yaml`
- `kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.4/ping_pong/manifests/service.yaml`
- `kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.4/ping_pong/manifests/statefulset.yaml`
- `kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.4/ping_pong/manifests/pingpong-analysis-template.yaml`
- `kubectl apply -f https://raw.githubusercontent.com/classroom-dee/hobbernetes/4.4/ping_pong/manifests/pingpong-rollout.yaml`
3. Edit analysis so the cpu limit is super tight
- 'value' section -> 0.001
- Modify rollout's template.metadata.annotations value to anything other than current value
4. Watch it go
- `kubectl argo rollouts get rollout ping-pong-dep -n exercises --watch`
- 1 pod will run for the new revision (25%)
- The second revision will use new analysis limit 0.001
- It will fail and give the rev2 pod back to rev1
- Done!

### Notes
- analysis run stat can be checked from `kubectl get analysisrun.argoprog.io -n exercises -w`