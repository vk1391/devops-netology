1.
```
vagrant@vagrant:/home$ kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4 --replicas=2
vagrant@vagrant:/home$ kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
hello-node   2/2     2            2           17s
vagrant@vagrant:/home$ kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-6d5f754cc9-n6cz9   1/1     Running   0          50s
hello-node-6d5f754cc9-rx6ff   1/1     Running   0          50s
```
3.
``` 
vagrant@vagrant:/home$ kubectl -n default scale --replicas=5 deploy hello-node
deployment.apps/hello-node scaled
vagrant@vagrant:/home$ kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
hello-node   5/5     5            5           8m30s
vagrant@vagrant:/home$ kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-6d5f754cc9-b574r   1/1     Running   0          21s
hello-node-6d5f754cc9-drxjn   1/1     Running   0          21s
hello-node-6d5f754cc9-n6cz9   1/1     Running   0          8m41s
hello-node-6d5f754cc9-rx6ff   1/1     Running   0          8m41s
hello-node-6d5f754cc9-v5pkh   1/1     Running   0          21s
```

2.
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /home/vagrant/.minikube/ca.crt
    extensions:
    - extension:
        last-update: Mon, 19 Sep 2022 18:07:11 UTC
        provider: minikube.sigs.k8s.io
        version: v1.26.1
      name: cluster_info
    server: https://192.168.49.2:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    extensions:
    - extension:
        last-update: Mon, 19 Sep 2022 18:07:11 UTC
        provider: minikube.sigs.k8s.io
        version: v1.26.1
      name: context_info
    namespace: default
    user: minikube
  name: minikube
- context:
    cluster: kubernetes
    user: user1
  name: user1-context
- context:
    cluster: minikube
    namespace: default
    user: user4
  name: user4-context
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /home/vagrant/.minikube/profiles/minikube/client.crt
    client-key: /home/vagrant/.minikube/profiles/minikube/client.key
- name: user4
  user:
    client-certificate: /home/vagrant/user4.crt
    client-key: /home/vagrant/user4.key
```
```
vagrant@vagrant:~$ kubectl --context=user4-context describe pod hello-node-6d5f754cc9-b574r
Name:             hello-node-6d5f754cc9-b574r
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Mon, 19 Sep 2022 18:25:33 +0000
Labels:           app=hello-node
                  pod-template-hash=6d5f754cc9
Annotations:      <none>
Status:           Running
IP:               172.17.0.10
IPs:
  IP:           172.17.0.10
Controlled By:  ReplicaSet/hello-node-6d5f754cc9
Containers:
  echoserver:
    Container ID:   docker://d55a1da43a77189fc360b6f710e16291dfa51838fd3a2f42755456e2415d7fb2
    Image:          k8s.gcr.io/echoserver:1.4
    Image ID:       docker-pullable://k8s.gcr.io/echoserver@sha256:5d99aa1120524c801bc8c1a7077e8f5ec122ba16b6dda1a5d3826057f67b9bcb
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Mon, 19 Sep 2022 18:25:34 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-rh9wl (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-rh9wl:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:                      <none>
```
