## 5.7 Deploy to serverless

### Usage
1. Start k3d 
- `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/chapter6/service-mesh/start_k3d.sh)`

2. Install kn cli + operator
- `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/chapter6/knative/install_knative.sh)`

3. Test the example app
- `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.7/ping_pong/deploy_as_serverless.sh)`

4. Make requests to the app until you get responses from both revisions
- `curl $(kubectl get ksvc -o jsonpath='{.items[0].status.url}' -n exercises)`
- On log will start with V2, the other with V1 and ping counts will diverge

5. Clean up
```bash
rm kn \
  && rm -r ~/.config/kn/plugins/kn-operator \
  && k3d cluster delete
```
