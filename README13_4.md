1. Необходимо упаковать приложение в чарт для деплоя в разные окружения. Требования:

 - каждый компонент приложения деплоится отдельным deployment’ом/statefulset’ом;
 - в переменных чарта измените образ приложения для изменения версии.
```
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
  namespace: test
  name: db
spec:
  selector:
    app: db
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
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
              value: postgres://user:password@db:5432
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
kind: StatefulSet
metadata:
  namespace: test
  name: db
spec:
  selector:
    matchLabels:
      app: db
  serviceName: db
  replicas: 1
  template:
    metadata:
      labels:
        app: db
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: db
        image: postgres:13-alpine
        ports:
        - containerPort: 5432
        env:
          - name: POSTGRES_PASSWORD
            value: postgres
        
          - name: POSTGRES_USER
            value: postgres
        
          - name: POSTGRES_DB
            value: news
```

2. Подготовив чарт, необходимо его проверить. Попробуйте запустить несколько копий приложения

 -  создал в дефолтном namespace test 
 `helm install rel1.0 myapp` 
 -  создал в namespace test1
`helm install rel1.1 myapp --set namespace=test1`
 - создал копию в дефолтном неймспейсе test
`helm install rel1.2 myapp --set backendName=back --set frontendName=front --set statefulset.name=db1` 

 - результат
```
vagrant@vagrant:~$ kubectl get pods -n test
NAME                                  READY   STATUS    RESTARTS   AGE
back-58c4c9894c-8k8s4                 1/1     Running   0          3m19s
backend-775cc76d75-27wll              1/1     Running   0          17m
db-0                                  1/1     Running   0          17m
db1-0                                 1/1     Running   0          3m19s
front-865c6b96ff-4vb6h                0/1     Running   0          3m19s
frontend-748b68556d-5jq9f             1/1     Running   0          17m
nfs-server-nfs-server-provisioner-0   1/1     Running   0          41m

vagrant@vagrant:~$ kubectl get pods -n test1
NAME                        READY   STATUS    RESTARTS   AGE
backend-775cc76d75-8mvpp    1/1     Running   0          17m
db-0                        1/1     Running   0          17m
frontend-748b68556d-kx26r   1/1     Running   0          17m

vagrant@vagrant:~$ helm list
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
nfs-server      test            1               2022-11-08 11:54:34.319173 +0000 UTC    deployed        nfs-server-provisioner-1.1.3    2.3.0      
rel1.0          test            1               2022-11-08 12:18:41.066088016 +0000 UTC deployed        myapp-0.1.1                     0.1.1      
rel1.1          test            1               2022-11-08 12:18:53.575059045 +0000 UTC deployed        myapp-0.1.1                     0.1.1      
rel1.2          test            1               2022-11-08 12:32:28.244922295 +0000 UTC deployed        myapp-0.1.1                     0.1.1      
```

