# Suggested values: advanced users of Kubernetes and Helm should feel
# free to use different values.
set -x
JHUB_RELEASE=jhub2
REDIS_RELEASE=redis2
NAMESPACE=jhub2

helm upgrade --install $JHUB_RELEASE ./jupyterhub \
  --namespace $NAMESPACE  \
  --version=0.8.0 \
  --recreate-pods \
  --values jhub-config.yml

helm upgrade --install $REDIS_RELEASE stable/redis \
    --namespace $NAMESPACE \
    --set master.service.type=LoadBalancer \
    --recreate-pods

kubectl create clusterrolebinding jhub-admin --clusterrole=cluster-admin --serviceaccount=jhub:hub

export REDIS_PASSWORD=$(kubectl get secret --namespace ${NAMESPACE} ${REDIS_RELEASE} -o jsonpath="{.data.redis-password}" | base64 --decode)
export SERVICE_IP=$(kubectl get svc --namespace ${NAMESPACE} ${REDIS_RELEASE}-master --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")

kubectl create secret generic redis --from-literal=redis_password=${REDIS_PASSWORD} --namespace ${NAMESPACE}
