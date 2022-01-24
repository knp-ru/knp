Install using helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install monitoring bitnami/kube-prometheus -n monitoring --create-namespace --set alertmanager.enabled=false,prometheus.persistence.enabled=true,prometheus.resources.requests.cpu=30m,prometheus.resources.requests.memory=512Mi,exporters.node-exporter.enabled=false,kubelet.enabled=false,kubeApiServer.enabled=false,kubeControllerManager.enabled=false,kubeScheduler.enabled=false,coreDns.enabled=false,kubeProxy.enabled=false
```
