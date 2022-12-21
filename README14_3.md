# Домашнее задание к занятию "14.3 Карты конфигураций"

## Задача 1: Работа с картами конфигураций через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать карту конфигураций?

```
vagrant@vagrant:~$ kubectl create configmap nginx-config --from-file=/home/vagrant/.kube/nginx.conf
configmap/nginx-config created
vagrant@vagrant:~$ kubectl create configmap domain --from-literal=name=netology.ru
configmap/domain created
```

### Как просмотреть список карт конфигураций?

```
vagrant@vagrant:~$ kubectl get configmaps
NAME               DATA   AGE
domain             1      21s
kube-root-ca.crt   1      43d
nginx-config       1      45s
vault-config       1      29h
```
```
vagrant@vagrant:~$ kubectl get configmap
NAME               DATA   AGE
domain             1      36s
kube-root-ca.crt   1      43d
nginx-config       1      60s
vault-config       1      29h
```

### Как просмотреть карту конфигурации?

```
vagrant@vagrant:~$ kubectl get configmap nginx-config
NAME           DATA   AGE
nginx-config   1      116s
vagrant@vagrant:~$kubectl describe configmap domain
Name:         domain
Namespace:    test
Labels:       <none>
Annotations:  <none>

Data
====
name:
----
netology.ru

BinaryData
====

Events:  <none>
```

### Как получить информацию в формате YAML и/или JSON?

```
vagrant@vagrant:~$ kubectl get configmap nginx-config -o yaml
apiVersion: v1
data:
  nginx.conf: |-
    server {
        listen 80;
        server_name  netology.ru www.netology.ru;
        access_log  /var/log/nginx/domains/netology.ru-access.log  main;
        error_log   /var/log/nginx/domains/netology.ru-error.log info;
        location / {
            include proxy_params;
            proxy_pass http://10.10.10.10:8080/;
        }
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2022-12-21T13:22:35Z"
  name: nginx-config
  namespace: test
  resourceVersion: "8118145"
  uid: f97d9964-808b-4ba5-9d00-bfa05a929445
```
```
vagrant@vagrant:~$ kubectl get configmap domain -o json
{
    "apiVersion": "v1",
    "data": {
        "name": "netology.ru"
    },
    "kind": "ConfigMap",
    "metadata": {
        "creationTimestamp": "2022-12-21T13:22:59Z",
        "name": "domain",
        "namespace": "test",
        "resourceVersion": "8118201",
        "uid": "8b887e03-3a48-45f1-a05f-9dcd1922155c"
    }
}
```

### Как выгрузить карту конфигурации и сохранить его в файл?

```
kubectl get configmaps -o json > configmaps.json
kubectl get configmap nginx-config -o yaml > nginx-config.yml
```

### Как удалить карту конфигурации?

```
kubectl delete configmap nginx-config
```

### Как загрузить карту конфигурации из файла?

```
kubectl apply -f nginx-config.yml
```
