# Suggested values: advanced users of Kubernetes and Helm should feel
# free to use different values.
set -x
RELEASE=jhub
NAMESPACE=jhub

helm upgrade --install $RELEASE jupyterhub/jupyterhub \
  --namespace $NAMESPACE  \
  --version=0.8.0 \
  --recreate-pods \
  --values jhub-config.yml

#helm upgrade --install redis stable/redis \
#    --namespace jhub \
#    --set master.service.type=LoadBalancer \
#    --recreate-pods

kubectl create clusterrolebinding jhub-admin --clusterrole=cluster-admin --serviceaccount=jhub:hub

export REDIS_PASSWORD=$(kubectl get secret --namespace jhub redis -o jsonpath="{.data.redis-password}" | base64 --decode)
export SERVICE_IP=$(kubectl get svc --namespace jhub redis --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
