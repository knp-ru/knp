Create a static IP address

```bash
gcloud compute addresses create knp-services --region us-central1
```

Install using helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install nginx-ingress-controller bitnami/nginx-ingress-controller -n nginx-ingress-controller --create-namespace --set metrics.enabled=true,metrics.serviceMonitor.enabled=true,defaultBackend.enabled=false,service.loadBalancerIP=$(gcloud compute addresses describe knp-services --region us-central1 | head -n1 | cut -d" " -f2)
```
