1. В stage окружении часто возникает необходимость отдавать статику бекенда сразу фронтом. Проще всего сделать это через общую папку. Требования:

 - в поде подключена общая папка между контейнерами (например, /static);
 - после записи чего-либо в контейнере с беком файлы можно получить из контейнера с фронтом.

yaml стейджа из предыдущего занятия с правками
```
apiVersion: apps/v1
kind: Deployment
metadata:
 name: fb-pod
spec:
 replicas: 1
 selector:
   matchLabels:
     app: fb_app1
 template:
   metadata:
     labels:
       app: fb_app1
   spec:
     containers:
     - name: frontend
       image: avloton/13-kube-frontend
       imagePullPolicy: IfNotPresent
       volumeMounts:
         - mountPath: "/share"
           name: share
       resources:
         limits:
           memory: "512Mi"
           cpu: "500m"
       ports:
       - containerPort: 80
     - name: backend
       image: avloton/13-kube-backend
       imagePullPolicy: IfNotPresent
       volumeMounts:
         - mountPath: "/tmp/cache"
           name: share
       resources:
         limits:
           memory: "512Mi"
           cpu: "500m"
       ports:
       - containerPort: 9000
     volumes:
       - name: share
         emptyDir: {}
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
 - Результат
```
NAME                                  READY   STATUS    RESTARTS   AGE
fb-pod-6c4bf95888-5c4kv               2/2     Running   0          7s
nfs-server-nfs-server-provisioner-0   1/1     Running   0          42m

vagrant@vagrant:~$ kubectl exec fb-pod-6c4bf95888-5c4kv -c backend -- sh -c 'echo "Hello!!!" > /tmp/cache/hello.txt'
vagrant@vagrant:~$ kubectl exec fb-pod-6c4bf95888-5c4kv -c frontend -- ls -al /share
total 12
drwxrwxrwx 2 root root 4096 Nov  1 08:17 .
drwxr-xr-x 1 root root 4096 Nov  1 08:14 ..
-rw-r--r-- 1 root root    9 Nov  1 08:17 hello.txt
vagrant@vagrant:~$ kubectl exec fb-pod-6c4bf95888-5c4kv -c frontend -- sh -c 'cat /share/hello.txt'
Hello!!!
vagrant@vagrant:~$ 
```
2. Поработав на stage, доработки нужно отправить на прод. В продуктиве у нас контейнеры крутятся в разных подах, поэтому потребуется PV и связь через PVC. Сам PV должен быть связан с NFS сервером. Требования:

 - все бекенды подключаются к одному PV в режиме ReadWriteMany;
 - фронтенды тоже подключаются к этому же PV с таким же режимом;
 - файлы, созданные бекендом, должны быть доступны фронту.

yaml прода из предыдущего занятия с правками
```
front.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  selector:
    app: frontend
  ports:
    - port: 80
  type: ClusterIP  
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
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
          volumeMounts:
          - name: secretdata
            mountPath: /mnt/nfs
      volumes:
        - name: secretdata
          persistentVolumeClaim:
            claimName: prod-share
```
```
back.yml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend
  ports:
    - port: 9000
  type: ClusterIP  
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
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
          image: avloton/13-kube-backend
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
          volumeMounts:
          - name: secretdata
            mountPath: /mnt/nfs
      volumes:
      - name: secretdata
        persistentVolumeClaim:
          claimName: prod-share   
```
```
pvc.yml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: prod-share
spec:
  storageClassName: "nfs"
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
```
 - Результат
```
vagrant@vagrant:~/.kube$ kubectl get pod
NAME                                  READY   STATUS    RESTARTS   AGE
backend-c66bb6f7b-hfbb4               1/1     Running   0          16s
frontend-5b7c845876-gk6d9             1/1     Running   0          16s
nfs-server-nfs-server-provisioner-0   1/1     Running   0          111m

vagrant@vagrant:~/.kube$ kubectl exec frontend-5b7c845876-gk6d9 -c frontend -- sh -c 'echo "HELLO!!!" > /mnt/nfs/hello.txt'
vagrant@vagrant:~/.kube$ kubectl exec frontend-5b7c845876-gk6d9 -c frontend -- ls -al /mnt/nfs
total 12
drwxrwsrwx 2 root root 4096 Nov  1 09:26 .
drwxr-xr-x 1 root root 4096 Nov  1 09:22 ..
-rw-r--r-- 1 root root    9 Nov  1 09:26 hello.txt
vagrant@vagrant:~/.kube$ kubectl exec frontend-5b7c845876-gk6d9 -c frontend -- cat /mnt/nfs/hello.txt
HELLO!!!
vagrant@vagrant:~/.kube$ kubectl exec backend-c66bb6f7b-hfbb4 -c backend -- ls -al /mnt/nfs
total 12
drwxrwsrwx 2 root root 4096 Nov  1 09:26 .
drwxr-xr-x 1 root root 4096 Nov  1 09:22 ..
-rw-r--r-- 1 root root    9 Nov  1 09:26 hello.txt
vagrant@vagrant:~/.kube$ kubectl exec backend-c66bb6f7b-hfbb4 -c backend -- cat /mnt/nfs/hello.txt
HELLO!!!
```
