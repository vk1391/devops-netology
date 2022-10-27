1.
```
secretsmysql.yaml

MYSQL_PASSWORD=password
MYSQL_DATABASE=db
MYSQL_ROOT_PASSWORD=password
MYSQL_USER=user

servicesmysql.yaml

apiVersion: v1
kind: Service
metadata:
  name: mysql
 
spec:
  # Open port 3306 only to pods in cluster
  selector:
    app: mysql-container
 
  ports:
    - name: mysql
      port: 3306
      protocol: TCP
      targetPort: 3306
  type: ClusterIP

storagemysql.yaml

apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
 
  name: localstorage
 
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: Immediate
reclaimPolicy: Delete
allowVolumeExpansion: True
 
---
 
kind: PersistentVolume
apiVersion: v1
metadata:
  name: mysql-01
  labels:
    type: local
spec:
  storageClassName: localstorage
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/mysql01"
    type: DirectoryOrCreate
---
kind: PersistentVolume
apiVersion: v1
metadata:
  name: mysql-02
  labels:
    type: local
spec:
  storageClassName: localstorage
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/mysql02"
    type: DirectoryOrCreate

mysqlsts.yaml

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-container
spec:
  serviceName: mysql
  replicas: 2
  selector:
    matchLabels:
      app: mysql-container
  template:
    metadata:
      labels:
        app: mysql-container
    spec:
      containers:
      - name: mysql-container
        image: mysql:latest
        imagePullPolicy: "IfNotPresent"
        envFrom:
          - secretRef:
             name: prod-secrets
        ports:
        - containerPort: 3306
        # container (pod) path
        volumeMounts:
          - name: mysql-persistent-storage
            mountPath: /var/lib/mysql
 
        resources:
          requests:
            memory: 300Mi
            cpu: 400m
          limits:
            memory: 400Mi
            cpu: 500m
      restartPolicy: Always
 
  volumeClaimTemplates:
    - metadata:
        name: mysql-persistent-storage
      spec:
        storageClassName: localstorage
        accessModes: ["ReadWriteOnce"]
        resources:
         requests:
          storage: 5Gi
        selector:
         matchLabels:
          type: local
          
 frontbackdeploy.yaml
 
 # Config Stage Pod
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fb-pod
  labels:
    app: fb-app
spec:
  selector:
    matchLabels:
      app: fb-app
  template:
    metadata:
      labels:
        app: fb-app
    spec:
    # Config Containers
      containers:
      - name: front
        image: nginx:latest
        ports:
        - containerPort: 80
      - name: back
        image: debian
        command: ["sleep", "3600"]
---
# Config Service
apiVersion: v1
kind: Service
metadata:
  name: fb-svc
  labels:
    app: fb
spec:
  type: NodePort
  ports:
  - port: 80
    nodePort: 30080
  selector:
    app: fb

 ```
  - результат
 ```
 vagrant@vagrant:~/.kube$ kubectl get pods
NAME                      READY   STATUS    RESTARTS   AGE
fb-pod-7bdc5b4c8c-fvtnd   2/2     Running   0          11s
mysql-container-0         1/1     Running   0          9m53s
mysql-container-1         1/1     Running   0          9m52s
vagrant@vagrant:~/.kube$ kubectl get svc
NAME     TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
fb-svc   NodePort    10.233.58.75   <none>        80:30080/TCP   41s
mysql    ClusterIP   10.233.9.67    <none>        3306/TCP       14m
vagrant@vagrant:~/.kube$ kubectl get sts
NAME              READY   AGE
mysql-container   2/2     10m
vagrant@vagrant:~/.kube$ kubectl get pvc
NAME                                         STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-persistent-storage-mysql-container-0   Bound    mysql-01   5Gi        RWO            localstorage   14m
mysql-persistent-storage-mysql-container-1   Bound    mysql-02   5Gi        RWO            localstorage   10m
vagrant@vagrant:~/.kube$ kubectl get pv
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                             STORAGECLASS   REASON   AGE
mysql-01   5Gi        RWO            Retain           Bound    test/mysql-persistent-storage-mysql-container-0   localstorage            18m
mysql-02   5Gi        RWO            Retain           Bound    test/mysql-persistent-storage-mysql-container-1   localstorage            18m
```
