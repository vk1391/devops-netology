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
Нужно было создать правильную ветку и активировать V2 секрет что б заработало
```
client = hvac.Client(
...     url='http://10.233.75.27:8200',
...     token='s.XPcifB7G0AeDLWiiVvzdKvKJ',
... )
>>> client.is_authenticated()
True
>>> client.secrets.kv.v2.create_or_update_secret(
...     path='hvac',
...     secret=dict(netology='ig secret!!!'),
... )
{'request_id': '3c27a591-32c5-0951-29b2-3acb9cab3754', 'lease_id': '', 'renewable': False, 'lease_duration': 0, 'data': {'created_time': '2022-12-21T12:18:45.024549822Z', 'custom_metadata': None, 'deletion_time': '', 'destroyed': False, 'version': 3}, 'wrap_info': None, 'warnings': None, 'auth': None}
>>> client.secrets.kv.v2.read_secret_version(
...     path='hvac',
... )
{'request_id': '889343e4-7cee-c14a-8c5f-3078084835d5', 'lease_id': '', 'renewable': False, 'lease_duration': 0, 'data': {'data': {'netology': 'ig secret!!!'}, 'metadata': {'created_time': '2022-12-21T12:18:45.024549822Z', 'custom_metadata': None, 'deletion_time': '', 'destroyed': False, 'version': 3}}, 'wrap_info': None, 'warnings': None, 'auth': None}
```
