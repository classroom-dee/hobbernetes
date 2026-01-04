## 5.2 Service Mesh

### Usage
- Start the cluster & set kubeconfig `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/start_k3d.sh)`

- AND THEN install CLI: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/install_istio.sh)`

- Install the book app: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/install_book_app.sh)`

- Add the services to the mesh: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/add_to_mesh.sh)`

- Enforce auth policy: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/enfoce_auth_policy.sh)`

- Manage traffic: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/manage_traffic.sh)`

- Clean up: `source <(curl -fsSL https://raw.githubusercontent.com/classroom-dee/hobbernetes/5.2/chapter6/service-mesh/cleanup.sh)`