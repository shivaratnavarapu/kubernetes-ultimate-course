<h1 align="center">
  🚀 Kubernetes Ultimate Course
</h1>

### 🛠️ Installation Steps:
  - [Install Dependencies](#install-dependencies)
  - [Kubernetes initialization](#Kubernetes-initialization)

## Install Dependencies

These steps need to be executed on master and worker nodes

**1. Enable the networking modules and bridge network on both master and worker nodes**

```
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
  
modprobe overlay
modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

**2. Install dependency packages**

```
apt-get update
apt-get install net-tools -y apt-transport-https ca-certificates curl
```

**3. Install containerd runtime**

```
wget https://github.com/containerd/containerd/releases/download/v1.7.13/cri-containerd-1.7.13-linux-amd64.tar.gz
tar --no-overwrite-dir -C / -xzf  cri-containerd-1.7.13-linux-amd64.tar.gz
mkdir /etc/containerd
containerd config default > /etc/containerd/config.toml

sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

systemctl daemon-reload

systemctl restart containerd

systemctl enable containerd
```

**4. Install kubeadm, kubectl and kubelet packages**

```
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt install -y kubelet kubeadm kubectl
systemctl enable --now kubelet
systemctl start kubelet
```

## Kubernetes initialization

These steps need to be executed on master node

**1. Initialize master node**

```
kubeadm init --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12
```

Copy kubeconfig file to .kube directory

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

**2. Check the status of node and pods**
```
kubectl get nodes -o wide
kubectl get po --all-namespaces -o wide
```

We would see that node is in not ready state, and few coredns pods are in pending state. This is because, we have not configured the networking

**3.	Deploy flannel network CNI**

```
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

Now check the status of nodes and pods
```
kubectl get nodes -o wide
kubectl get po --all-namespaces -o wide
```

We would see that node is in ready state, and all pods are in running state


## Join worker nodes to the cluster

**1. Make sure you have installed the required dependencies on the worker node as mentioned in the "Install dependencies" section**
  - [Install Dependencies](#install-dependencies)
    
**2. Join the worker node to cluster**

If you have saved the join command that was generated when we do kubernetes initialization on master node, we can run the same join command.
In case if you forgot to save the join command, then regenerate the join command by executing below command on **master node**

```
kubeadm token create --print-join-command
```
THe above command will generate a kubeadm join command, this command need to be executed on worker node so that it joins the kuberentes cluster
