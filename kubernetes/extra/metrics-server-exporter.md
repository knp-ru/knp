Install from [here](https://github.com/olxbr/metrics-server-exporter).

Also add a service monitor:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: metrics-server-exporter
  namespace: kube-system
spec:
  endpoints:
    - interval: 30s
      port: metrics
  namespaceSelector:
    matchNames:
      - kube-system
  selector:
    matchLabels:
      k8s-app: metrics-server-exporter
```
