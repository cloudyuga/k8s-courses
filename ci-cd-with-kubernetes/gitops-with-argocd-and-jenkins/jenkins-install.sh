curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
sleep 3
echo "installed helm"

helm repo add jenkins https://charts.jenkins.io

kubectl create ns jenkins

helm install jenkins \
--set controller.serviceType=NodePort,controller.image=teamcloudyuga/cyjenkins,controller.tag=2.289,controller.installPlugins=false,controller.nodePort=30001,persistence.enabled=false \
--namespace=jenkins \
jenkins/jenkins
echo "installed jenkins with helm "
