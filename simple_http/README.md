## Log Output
### Usage
1. This demo uses port 8070 as input but you can change it.
2. Deploy with `kubectl create deployment simple-http --image=xuanminator/simple-http --dry-run=client -o yaml | kubectl set env --local -f - PORT=8070 -o yaml | kubectl apply -f -`
3. Open proxy with `kubectl port-forward deployment/simple-http 8070:8070`
4. Make request from client: `curl http://localhost:8070`