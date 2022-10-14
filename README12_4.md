Развернул на яндекс машинах
 - hosts.yaml
```
all:
  hosts:
    node1:
      ansible_host: 51.250.31.146
      ip: 10.129.0.23
     # access_ip: 51.250.31.146
     # ansible_user: root
    node2:
      ansible_host: 84.201.153.1
      ip: 10.129.0.35
      #access_ip: 84.201.153.1
     # ansible_user: root
    node3:
      ansible_host: 158.160.2.88
      ip: 10.129.0.19
 #     access_ip: 10.129.0.32
    #  ansible_user: root
    node4:
      ansible_host: 84.201.139.218
      ip: 10.129.0.36
    #  access_ip: 10.129.0.24
    #  ansible_user: root
    node5:
      ansible_host: 51.250.24.152
      ip: 10.129.0.22
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
        node4:
        node5:        
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
 - скрин с результатом
![screenshot](https://github.com/vk1391/devops-netology/blob/959dabffca2e366a949965bc38e1eb29c70a3873/%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5_2022-10-14_143130786.png)
