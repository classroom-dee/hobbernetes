## 4.3 Prometheus

1. Start:
- `./misc/setup.sh`: rollout is not needed but it happens to be in there so...
- Go to `http://locahost:9090`

2. Query: `count(kube_statefulset_created{namespace="prometheus"})`
It's 2 in my case :0 different chart? 🤷