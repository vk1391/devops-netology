sts vault
```
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vault
  labels:
    app: vault
spec:
  serviceName: "vault"
  selector:
    matchLabels:
      app: vault
  replicas: 1
  template:
    metadata:
      labels:
        app: vault
    spec:
      containers:
        - name: vault
          image: vault:1.9.0
          imagePullPolicy: IfNotPresent
          args:
            - "server"
            - "-config=/etc/vault/config/vault.hcl"
          ports:
            - name: http
              containerPort: 8200
              protocol: "TCP"
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
          securityContext:
            capabilities:
              add:
                - IPC_LOCK # разрешает делать системный вызов mlock без повышения привилегий контейнера, выделение памяти большими страницами
                - CAP_SETFCAP # нужно для мапинга юзер ид0 в нового пользака в неймпейсе ядра, вызов setcap
          volumeMounts:
            - name: config
              mountPath: /etc/vault/config
            - name: vault-data
              mountPath: /vault/data
      volumes:
        - name: config
          configMap:
            name: vault-config
  volumeClaimTemplates:
    - metadata:
        name: vault-data
      spec:
        accessModes: [ "ReadWriteOnce" ]
        storageClassName: "nfs"
        resources:
          requests:
            storage: 1Gi
```
svc vault 
```
---
apiVersion: v1
kind: Service
metadata:
  name: vault
spec:
  clusterIP: None
  ports:
    - name: http
      port: 8200
  selector:
    app: vault
 ```
 configmap vault
 ```
 ---
apiVersion: v1
kind: ConfigMap
metadata:
  name: vault-config
data:
  vault.hcl: |
    disable_mlock = true
    ui = true
    api_addr = "http://vault:8200"

    listener "tcp" {
      address = "[::]:8200"
      tls_disable = 1
      #tls_cert_file = "/vault/userconfig/tls-server/server.crt"
      #tls_key_file = "/vault/userconfig/tls-server/server.key"
      #tls_ca_cert_file = "/vault/userconfig/tls-ca/ca.crt"
    }
    storage "file" {
      path = "/vault/data"
    }
```
Запустил,проинициалилизировал вольт,запустил вторую машину, запустил предложеный скрипт

Вывод на скрипт,но мне кажеться это не самый верный результат
Проблемы с hvac?
```
sh-5.2# sudo ./script.py 
Traceback (most recent call last):
  File "//./script.py", line 10, in <module>
    client.secrets.kv.v2.create_or_update_secret(
  File "/usr/local/lib/python3.11/site-packages/hvac/api/secrets_engines/kv_v2.py", line 137, in create_or_update_secret
    return self._adapter.post(
           ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/hvac/adapters.py", line 125, in post
    return self.request("post", url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/hvac/adapters.py", line 356, in request
    response = super().request(*args, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/hvac/adapters.py", line 322, in request
    utils.raise_for_error(
  File "/usr/local/lib/python3.11/site-packages/hvac/utils.py", line 42, in raise_for_error
    raise exceptions.InvalidPath(message, errors=errors, method=method, url=url)
hvac.exceptions.InvalidPath: no handler for route 'secret/data/hvac', on post http://10.233.75.27:8200/v1/secret/data/hvac
```
