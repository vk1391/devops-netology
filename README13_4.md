1. Необходимо упаковать приложение в чарт для деплоя в разные окружения. Требования:

каждый компонент приложения деплоится отдельным deployment’ом/statefulset’ом;
в переменных чарта измените образ приложения для изменения версии.
```
helm template myapp
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /home/vagrant/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /home/vagrant/.kube/config
---
# Source: myapp/templates/sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
# Source: myapp/templates/storage.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv-claim
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
---
# Source: myapp/templates/storage.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
---
# Source: myapp/templates/back-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: test
spec:
  selector:
    app: backend
  ports:
    - port: 80
  type: ClusterIP
---
# Source: myapp/templates/front-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: test
spec:
  selector:
    app: frontend
  ports:
    - port: 80
  type: ClusterIP
---
# Source: myapp/templates/mysql-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
  namespace: test
spec:
  ports:
  - port: 3306
  selector:
    app: mysql
---
# Source: myapp/templates/back-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: nginx:latest
          env:
            - name: DATABASE_URL
              value: mysql://user:password@db:3306
          imagePullPolicy: IfNotPresent
          resources:
            limits:
              memory: "768Mi"
              cpu: "500m"
          ports:
            - containerPort: 9000
---
# Source: myapp/templates/front-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: avloton/13-kube-frontend
          env:
            - name: BASE_URL
              value: http://backend:9000
          imagePullPolicy: IfNotPresent
          resources:
            limits:
              memory: "768Mi"
              cpu: "500m"
          ports:
            - containerPort: 80
---
# Source: myapp/templates/mysql-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: test
spec:
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:latest
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: Admin
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
```

2. Подготовив чарт, необходимо его проверить. Попробуйте запустить несколько копий приложения
```
vagrant@vagrant:~$ helm install myapp2 myapp --set namespace=test2
vagrant@vagrant:~$ helm list
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /home/vagrant/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /home/vagrant/.kube/config
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
myapp2  test            1               2022-11-03 12:22:55.101630904 +0000 UTC deployed        myapp-0.1.1     0.1.1      
vagrant@vagrant:~$ kubectl get pods
No resources found in test namespace.
vagrant@vagrant:~$ kubectl get pods --namespace=test2
NAME                        READY   STATUS    RESTARTS   AGE
backend-54b5b449fb-hdwgz    1/1     Running   0          11m
frontend-748b68556d-k2cf7   1/1     Running   0          11m
mysql-97f6cf796-bx9ss       0/1     Pending   0          11m
vagrant@vagrant:~$ helm upgrade myapp2 myapp --set namespace=test
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /home/vagrant/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /home/vagrant/.kube/config
Release "myapp2" has been upgraded. Happy Helming!
NAME: myapp2
LAST DEPLOYED: Thu Nov  3 12:34:49 2022
NAMESPACE: test
STATUS: deployed
REVISION: 2
TEST SUITE: None
vagrant@vagrant:~$ kubectl get pods
NAME                        READY   STATUS    RESTARTS     AGE
backend-54b5b449fb-l2zmr    1/1     Running   0            8s
frontend-748b68556d-88ssb   1/1     Running   0            8s
mysql-97f6cf796-spjpf       1/1     Running   0            8s
```
