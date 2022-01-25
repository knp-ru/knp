Create a config map

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-ini
  namespace: monitoring
data:
  grafana.ini: |
    [server]
    domain = grafana.knp.services
    root_url = "http://%(domain)s/"

    [auth]
    disable_login_form = true

    [auth.github]
    enabled = true
    allow_sign_up = true
    client_id = 4fe2e3bdf8b3ba3f4c83
    client_secret = YOUR_SECRET
    scopes = user:email,read:org
    auth_url = https://github.com/login/oauth/authorize
    token_url = https://github.com/login/oauth/access_token
    api_url = https://api.github.com/user
    allowed_organizations = knp-ru

    [users]
    auto_assign_org_role = Admin
```

Install using helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install grafana bitnami/grafana -n monitoring --create-namespace --set persistence.size=4Gi,ingress.enabled=true,ingress.hostname=grafana.knp.services,ingress.ingressClassName=nginx,config.useGrafanaIniFile=true,config.grafanaIniConfigMap=grafana-ini
```
