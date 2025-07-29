## Ping Pong
### Usage
1. Shared ingress from log_output
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.7/log_output/manifests/ingress.yaml`
2. Secrets
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.7/ping_pong/manifests/secrets.yaml`
3. Deploy
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.7/ping_pong/manifests/statefulset.yaml`
   - `kubectl apply -f https://raw.githubusercontent.com/boolYikes/hobbernetes/2.7/ping_pong/manifests/service.yaml`
4. [Make request here](http://localhost:8081/pingpong) to increase ping count
5. Query: Decode the secret with base64 first
   - `kubectl run -it -n exercises --rm --restart=Never --image postgres:13 psql-test sh`
   - `psql -U <decoded username> -h ping-pong-stset-0.ping-pong-pg-svc -p 5432 -d postgres` then enter the decode pw
   - `select * from pings`