#!/bin/bash
kubeadm init --pod-network-cidr=10.244.0.0/16 --ignore-preflight-errors=all
sleep 2
mkdir -p /root/.kube
sudo cp -i /etc/kubernetes/admin.conf /root/.kube/config
export KUBECONFIG=/root/.kube/config && kubectl get nodes 
curl https://docs.projectcalico.org/manifests/calico.yaml -O
export KUBECONFIG=/root/.kube/config && kubectl apply -f calico.yaml
export KUBECONFIG=/root/.kube/config && kubectl taint nodes --all node-role.kubernetes.io/master-
sleep 2
export KUBECONFIG=/root/.kube/config && kubectl get nodes
echo "export KUBECONFIG=/root/.kube/config" >> /root/.bashrc
export KUBECONFIG=/root/.kube/config && kubectl apply -f /home/ubuntu/nginx-ingress-controller.yaml
export KUBECONFIG=/root/.kube/config && kubectl apply -f /home/ubuntu/local-path-storage.yaml
echo "source /etc/profile.d/bash_completion.sh" >> /root/.bashrc
echo 'source <(kubectl completion bash)' >> /root/.bashrc
echo 'alias k=kubectl' >> /root/.bashrc