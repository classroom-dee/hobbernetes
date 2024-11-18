# *THESE ARE TBD*
## Project Setup
## The Backbone
### I. Docker
DO NOT COPY PASTE THE WHOLE BLOCK LOL
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
### II. CRI-Dockerd
1. CHECK YOUR OS COMPAT!! Mine is Ubuntu 24.04 noble</br>
`*the mirantis doc goes here.* if it works, skip 2.`</br>
2. In this file:(It could pre-exist or be empty)</br>
`sudo nano /etc/docker/daemon.json`</br>
add this code:</br>
`{
  "exec-opts": ["native.cgroupdriver=systemd"]
}`</br>
then, execute:</br>
`sudo systemctl restart docker`</br>
3. finally, </br>
`sudo chmod 666 /var/run/cri-dockerd.sock`</br>
### III. Kubes
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
<strong>*THIS IS NOT PERSISTENT ACROSS REBOOTS*</strong>:</br>
`crictl config --set runtime-endpoint=unix:///var/run/cri-dockerd.sock`</br>
ii. `sudo systemctl start cri-docker`</br>
iii. `sudo systemctl enable cri-docker`</br>
iv. Switch to root for ease of use `sudo -i`</br>
v. *NOT PERSISTENT* : `sudo swapoff -a`</br>
vi. *Choose vi. alone OR vii. ~</br>
```bash
sudo kubeadm init \
--cri-socket unix:///var/run/cri-dockerd.sock \
--pod-network-cidr 10.244.0.0/16
```
vii.
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











