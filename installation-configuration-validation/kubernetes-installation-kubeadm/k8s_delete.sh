#!/bin/bash
kubeadm reset --force
rm -rf /etc/cni/net.d
rm -rf /root/.kube
