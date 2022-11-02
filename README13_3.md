1. Для проверки работы можно использовать 2 способа: port-forward и exec. Используя оба способа, проверьте каждый компонент:
 - сделайте запросы к бекенду;
 - сделайте запросы к фронту;
 - подключитесь к базе данных.

frontend port-forward
```
vagrant@vagrant:~/.kube$ kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
backend-db86d8d99-7nbt5     1/1     Running   0          13s
frontend-748b68556d-4z7sv   1/1     Running   0          27s
mysql-84d8f6d9fb-5lp25      1/1     Running   0          59m

kubectl port-forward frontend-748b68556d-4z7sv 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080

vagrant@vagrant:~/.kube$ curl 127.0.0.1:8080
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Список</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/build/main.css" rel="stylesheet">
</head>
<body>
    <main class="b-page">
        <h1 class="b-page__title">Список</h1>
        <div class="b-page__content b-items js-list"></div>
    </main>
    <script src="/build/main.js"></script>
</body>
</html>
```
frontend exec
```
kubectl exec frontend-748b68556d-4z7sv -- sh -c 'curl 127.0.0.1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   448  100   448    0     0   437k      0 --:--:-- --:--:-- --:--:--  437k
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Список</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/build/main.css" rel="stylesheet">
</head>
<body>
    <main class="b-page">
        <h1 class="b-page__title">Список</h1>
        <div class="b-page__content b-items js-list"></div>
    </main>
    <script src="/build/main.js"></script>
</body>
</html>
```  
backend port-forward
```
vagrant@vagrant:~/.kube$ kubectl port-forward backend-db86d8d99-7nbt5 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080

vagrant@vagrant:~/.kube$ curl 127.0.0.1:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
backend exec
```
kubectl exec backend-db86d8d99-7nbt5 -- sh -c 'curl 127.0.0.1'
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   615  100   615    0     0   600k      0 --:--:-- --:--:-- --:--:--  600k
```
mysql port-forward
```
^Cvagrant@vagrant:~/.kube$ kubectl port-forward mysql-84d8f6d9fb-5lp25 3307:3306
Forwarding from 127.0.0.1:3307 -> 3306
Forwarding from [::1]:3307 -> 3306
Handling connection for 3307
Handling connection for 3307
Handling connection for 3307

mysql --host=127.0.0.1 --port=3307 -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.6.51 MySQL Community Server (GPL)

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```
mysql exec
```
kubectl exec mysql-84d8f6d9fb-5lp25 -- sh -c 'mysql -u root -p'
Enter password: ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
command terminated with exit code 1
```

2. При работе с приложением иногда может потребоваться вручную добавить пару копий. Используя команду kubectl scale, попробуйте увеличить количество бекенда и фронта до 3. Проверьте, на каких нодах оказались копии после каждого действия (kubectl describe, kubectl get pods -o wide). После уменьшите количество копий до 1.

увеличил количество реплик фронтенда до 3
```
vagrant@vagrant:~/.kube$ kubectl scale --replicas=3 deployment frontend -n test
deployment.apps/frontend scaled
vagrant@vagrant:~/.kube$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
backend-db86d8d99-7nbt5     1/1     Running   0          8m44s   10.233.71.3   node3   <none>           <none>
frontend-748b68556d-44q5s   1/1     Running   0          18s     10.233.71.4   node3   <none>           <none>
frontend-748b68556d-4z7sv   1/1     Running   0          8m58s   10.233.75.4   node2   <none>           <none>
frontend-748b68556d-tldks   1/1     Running   0          18s     10.233.75.5   node2   <none>           <none>
mysql-84d8f6d9fb-5lp25      1/1     Running   0          67m     10.233.71.2   node3   <none>           <none>
vagrant@vagrant:~/.kube$ kubectl describe frontend
error: the server doesn't have a resource type "frontend"
vagrant@vagrant:~/.kube$ kubectl describe deploy frontend
Name:                   frontend
Namespace:              test
CreationTimestamp:      Wed, 02 Nov 2022 08:12:29 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=frontend
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=frontend
  Containers:
   frontend:
    Image:      avloton/13-kube-frontend
    Port:       80/TCP
    Host Port:  0/TCP
    Limits:
      cpu:     500m
      memory:  768Mi
    Environment:
      BASE_URL:  http://backend:9000
    Mounts:      <none>
  Volumes:       <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   frontend-748b68556d (3/3 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  9m31s  deployment-controller  Scaled up replica set frontend-748b68556d to 1
  Normal  ScalingReplicaSet  51s    deployment-controller  Scaled up replica set frontend-748b68556d to 3
  ```
  увеличил количество реплик backend до 3
  ```
  vagrant@vagrant:~/.kube$ kubectl scale --replicas=3 deployment backend -n test
deployment.apps/backend scaled
vagrant@vagrant:~/.kube$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
backend-db86d8d99-2b58b     1/1     Running   0          11s     10.233.71.5   node3   <none>           <none>
backend-db86d8d99-7nbt5     1/1     Running   0          11m     10.233.71.3   node3   <none>           <none>
backend-db86d8d99-t8nmc     1/1     Running   0          11s     10.233.75.6   node2   <none>           <none>
frontend-748b68556d-44q5s   1/1     Running   0          2m53s   10.233.71.4   node3   <none>           <none>
frontend-748b68556d-4z7sv   1/1     Running   0          11m     10.233.75.4   node2   <none>           <none>
frontend-748b68556d-tldks   1/1     Running   0          2m53s   10.233.75.5   node2   <none>           <none>
mysql-84d8f6d9fb-5lp25      1/1     Running   0          70m     10.233.71.2   node3   <none>           <none>
vagrant@vagrant:~/.kube$ kubectl describe deploy backend
Name:                   backend
Namespace:              test
CreationTimestamp:      Wed, 02 Nov 2022 08:12:43 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=backend
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=backend
  Containers:
   backend:
    Image:      nginx:latest
    Port:       80/TCP
    Host Port:  0/TCP
    Limits:
      cpu:     500m
      memory:  768Mi
    Environment:
      DATABASE_URL:  mysql://user:password@db:3306
    Mounts:          <none>
  Volumes:           <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   backend-db86d8d99 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  11m   deployment-controller  Scaled up replica set backend-db86d8d99 to 1
  Normal  ScalingReplicaSet  20s   deployment-controller  Scaled up replica set backend-db86d8d99 to 3
  ```
  вернул по одной реплике
  ```
  vagrant@vagrant:~/.kube$ kubectl scale --replicas=1 deployment backend -n test
deployment.apps/backend scaled
vagrant@vagrant:~/.kube$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
backend-db86d8d99-t8nmc     1/1     Running   0          110s    10.233.75.6   node2   <none>           <none>
frontend-748b68556d-44q5s   1/1     Running   0          4m32s   10.233.71.4   node3   <none>           <none>
frontend-748b68556d-4z7sv   1/1     Running   0          13m     10.233.75.4   node2   <none>           <none>
frontend-748b68556d-tldks   1/1     Running   0          4m32s   10.233.75.5   node2   <none>           <none>
mysql-84d8f6d9fb-5lp25      1/1     Running   0          71m     10.233.71.2   node3   <none>           <none>
vagrant@vagrant:~/.kube$ kubectl scale --replicas=1 deployment frontend -n test
deployment.apps/frontend scaled
vagrant@vagrant:~/.kube$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
backend-db86d8d99-t8nmc     1/1     Running   0          2m5s    10.233.75.6   node2   <none>           <none>
frontend-748b68556d-44q5s   1/1     Running   0          4m47s   10.233.71.4   node3   <none>           <none>
mysql-84d8f6d9fb-5lp25      1/1     Running   0          72m     10.233.71.2   node3   <none>           <none>
```
