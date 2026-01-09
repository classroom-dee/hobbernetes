## 5.6 Trying serverless

### Usage
1. Start k3d 
- `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.6/chapter6/service-mesh/start_k3d.sh)`

2. Install kn cli + operator
- `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.6/chapter6/knative/install_knative.sh)`

3. Test the example app
- `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.6/chapter6/knative/example_apps.sh)`

4. Make request to the app until you get responses from both revisions
- `curl $(kubectl get ksvc -o jsonpath='{.items[0].status.url}')`

5. Clean up
```bash
rm kn \
  && rm -r ~/.config/kn/plugins/kn-operator \
  && k3d cluster delete
```
