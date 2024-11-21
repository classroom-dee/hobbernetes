# *THESE ARE TBD*
## Environment
- Master node: Ubuntu 24.04 server on Hyper-V on Windows 10 Pro
- Worker node: Ubuntu 24.04 server on a baremetal, dedicated server
- Networking: All nodes on WAN connection behind a simple router.
## Setup Overview
## The Backbone
### I. Hyper-V
i. Host setup
- This will be the master node.
- Req: Win 10 Pro or NT?
- In Bios, enable virtualization(method varies).
- Enable the feature on Hyper Visor Manager, restart PC
ii. VM
- *External Switch* for the network adaptor
- *Dynamic Memory* minimum set to 4GB
- *CPUs* set to at least 2: check `htop` or `lscpu` to confirm the number of cpus. If the setting's not working, refer to Hyper-V docs.
### II. Host machine settings
Applies to master and worker nodes alike from here on out!</br>
i. Host config</br>
Get the network interface's ipv4 address of ALL NODES. Mines are 192.168.0.8 and 100.</br>
`sudo vi /etc/hosts`</br>
then, add:
```plaintext
...
192.168.0.8 master
192.168.0.100 worker-01
...
```
ii. Firewalls</br>
Disable the frontend firewall. For Redhat base OS, it's firewalld.</br>
```bash
sudo ufw disable
sudo systemctl stop ufw
sudo systemctl disable ufw
sudo systemctl mask --now ufw
```
then,
```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
```
then,
```bash
sudo sysctl --system
```


### III. Docker
*DO NOT COPY PASTE THE WHOLE BLOCK* LOL
```bash
# DO NOT remove containerd. it might ship as default on you distro

# check for old packages
 for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# and then, clean it up
sudo rm -rf /var/lib/docker 
# update repo and then install
sudo apt-get update
sudo apt-get install ca-certificates curl
# secrets
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# install the package
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# then"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```
### IV. CRI-Dockerd
1. CHECK YOUR OS COMPAT!! Mine is Ubuntu 24.04 noble</br>
Excerpt from the Mirantis doc.</br>
```shell
git clone https://github.com/Mirantis/cri-dockerd.git
# STOP and install golang : https://go.dev/doc/install
# ONCE DONE,
cd cri-dockerd
ARCH=amd64 make cri-dockerd
sudo mkdir -p /usr/local/bin
sudo install -o root -g root -m 0755 cri-dockerd /usr/local/bin/cri-dockerd
sudo install packaging/systemd/* /etc/systemd/system
sudo sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service
sudo systemctl daemon-reload
sudo systemctl enable --now cri-docker.socket
```
then, inside `sudo nano /etc/systemd/system/multi-user.target.wants/cri-docker.service` edit line,</br>
```yaml
ExecStart=/usr/local/bin/cri-dockerd --container-runtime-endpoint fd:// --network-plugin=cni --pod-cidr=10.244.0.0/16
```
then,</br>
`sudo systemctl daemon-reload`
2. DO THIS ONLY IF `docker info | grep Cgroup` shows `cgroupfs`, not `systemd`</br>
In this file:(It could pre-exist or be empty)</br>
`sudo nano /etc/docker/daemon.json`</br>
add this code:</br>
`{
  "exec-opts": ["native.cgroupdriver=systemd"]
}`</br>
then, execute:</br>
`sudo systemctl restart docker`</br>
3. finally, </br>
`sudo chmod 666 /var/run/cri-dockerd.sock`</br>
### V. Kubes
```bash
# update repos
sudo apt-get update
# install dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
# secrets
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
# add repo
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
# update repo
sudo apt-get update
# install cores
sudo apt-get install -y kubelet kubeadm kubectl
# version fixed
sudo apt-mark hold kubelet kubeadm kubectl
```
### IV. Masternode Init
    a. Decide which network add-on to use.
    b. The network add-on will have instructions on which CIDR to use.
    c. Use that to specify init's CIDR parameter.
    d. If using Docker Engine, don't forget the Unix socket parameter for cri-dockerd
    e. Always do dry run first so you don't have to reset and start all over again ...
i. 
`crictl config --set runtime-endpoint=unix:///var/run/cri-dockerd.sock`</br>
ii. `sudo systemctl start cri-docker`</br>
iii. `sudo systemctl enable cri-docker`</br>
iv. Switch to root for ease of use `sudo -i`</br>
v. `sudo sed -i '/swap/d' /etc/fstab` and then *reboot*</br>
vi. Init CP</br>
```bash
sudo kubeadm init \
--cri-socket unix:///var/run/cri-dockerd.sock \
--pod-network-cidr 10.244.0.0/16
```
### V. Kubectl config
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
### VI. Network plugin
`kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/tigera-operator.yaml`</br>
then, </br>
`wget https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/custom-resources.yaml`</br>
then,</br>
`nano custom-resources.yaml`</br>
and edit line: </br>
`cidr: 10.244.0.0/16`</br>
confirm pods running:</br>
`watch kubectl get pods -n calico-system`</br>
"taint" nodes, which means to make a node available for pods</br>
`kubectl taint nodes --all node-role.kubernetes.io/control-plane-`</br>
confirm node exposure:</br>
`kubectl get nodes -o wide`</br>


## NOT-USED Settings
THESE WERE USED RIGHT BEFORE INIT</br>
vi.
```yaml
# write a config anywhere
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
nodeRegistration:
  criSocket: /var/run/cri-dockerd.sock
```
```bash
# run this to render the config up-to-date\
sudo kubeadm config migrate --old-config old.yaml --new-config new.yaml
```
```yaml
# and open new.yaml, add under the networking section under the clusterconfig:
podSubnet: 10.244.0.0/16
# and add new lines at the bottom, including the hypens
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
containerRuntimeEndpoint: unix:///var/run/cri-dockerd.sock
```
vii. Kubelet related (prolly should be set after init or join is done)
```bash
## pause image : this seems to be deprecated
# kubelet --pod-infra-container-image=registry.k8s.io/pause:3.10
## In here:
sudo nano /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
## edit line:
Environment="KUBELET_EXTRA_ARGS=--pod-infra-container-image=registry.k8s.io/pause:3.9"
```
viii. The core
```bash
kubeadm init \
# --dry-run \ # for testing
--config "path/to/previously/made/new.yaml" \
```
- On failure for some reason, fix the issue and `sudo kubeadm reset` and then do over
- Set up kubelet, kubectl
- Replicate the process on other node, this time with `join`











