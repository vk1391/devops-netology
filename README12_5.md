1. Установить в кластер CNI плагин Calico
 - hosts.yaml
 ```
 all:
  hosts:
    node1:
      ansible_host: 84.252.138.46
      ip: 10.129.0.18
     # access_ip: 51.250.31.146
     # ansible_user: root
    node2:
      ansible_host: 84.252.141.1
      ip: 10.129.0.30
      #access_ip: 84.201.153.1
     # ansible_user: root
    node3:
      ansible_host: 130.193.53.201
      ip: 10.129.0.12
 #     access_ip: 10.129.0.32
    #  ansible_user: root
    #node4:
     # ansible_host: 84.201.139.218
    #  ip: 10.129.0.36
    #  access_ip: 10.129.0.24
    #  ansible_user: root
 #  node5:
  #    ansible_host: 51.250.24.152
  #    ip: 10.129.0.22
     # access_ip: 10.129.0.15
     # ansible_user: root
  children:
    kube_control_plane:
      hosts:
        node1:
    kube_node:
      hosts:
        node2:
        node3:       
    etcd:
      hosts:
        node1:
    k8s_cluster:
      children:
        kube_control_plane:
        kube_node:
    calico_rr:
      hosts: {}
```
 - нашёл пример nginx и проверил
 ```
vagrant@vagrant:~/kubespray$ kubectl create -f - <<EOF
> kind: NetworkPolicy
> apiVersion: networking.k8s.io/v1
> metadata:
>   name: access-nginx
>   namespace: policy-demo
> spec:
>   podSelector:
>     matchLabels:
>       app: nginx
>   ingress:
>     - from:
>       - podSelector:
>           matchLabels:
>             run: access
> EOF
networkpolicy.networking.k8s.io/access-nginx created
vagrant@vagrant:~/kubespray$ kubectl run --namespace=policy-demo access --rm -ti --image busybox /bin/sh
If you don't see a command prompt, try pressing enter.
/ # wget -q --timeout=5 nginx -O -
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
2. изучить, что запущено по умолчанию
```
vagrant@vagrant:~$ calicoctl get nodes --allow-version-mismatch
NAME    
node1   
node2   
node3   

vagrant@vagrant:~$ calicoctl get ipPool --allow-version-mismatch
NAME           CIDR             SELECTOR   
default-pool   10.233.64.0/18   all()      

vagrant@vagrant:~$ calicoctl get profile --allow-version-mismatch
NAME                                                 
projectcalico-default-allow                          
kns.default                                          
kns.kube-node-lease                                  
kns.kube-public                                      
kns.kube-system                                      
kns.policy-demo                                      
ksa.default.default                                  
ksa.kube-node-lease.default                          
ksa.kube-public.default                              
ksa.kube-system.attachdetach-controller              
ksa.kube-system.bootstrap-signer                     
ksa.kube-system.calico-kube-controllers              
ksa.kube-system.calico-node                          
ksa.kube-system.certificate-controller               
ksa.kube-system.clusterrole-aggregation-controller   
ksa.kube-system.coredns                              
ksa.kube-system.cronjob-controller                   
ksa.kube-system.daemon-set-controller                
ksa.kube-system.default                              
ksa.kube-system.deployment-controller                
ksa.kube-system.disruption-controller                
ksa.kube-system.dns-autoscaler                       
ksa.kube-system.endpoint-controller                  
ksa.kube-system.endpointslice-controller             
ksa.kube-system.endpointslicemirroring-controller    
ksa.kube-system.ephemeral-volume-controller          
ksa.kube-system.expand-controller                    
ksa.kube-system.generic-garbage-collector            
ksa.kube-system.horizontal-pod-autoscaler            
ksa.kube-system.job-controller                       
ksa.kube-system.kube-proxy                           
ksa.kube-system.namespace-controller                 
ksa.kube-system.node-controller                      
ksa.kube-system.nodelocaldns                         
ksa.kube-system.persistent-volume-binder             
ksa.kube-system.pod-garbage-collector                
ksa.kube-system.pv-protection-controller             
ksa.kube-system.pvc-protection-controller            
ksa.kube-system.replicaset-controller                
ksa.kube-system.replication-controller               
ksa.kube-system.resourcequota-controller             
ksa.kube-system.root-ca-cert-publisher               
ksa.kube-system.service-account-controller           
ksa.kube-system.service-controller                   
ksa.kube-system.statefulset-controller               
ksa.kube-system.token-cleaner                        
ksa.kube-system.ttl-after-finished-controller        
ksa.kube-system.ttl-controller                       
ksa.policy-demo.default          
```
