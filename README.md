1.
```
route-views>show ip route 217.197.228.106
Routing entry for 217.197.224.0/20, supernet
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 3w1d ago
  Routing Descriptor Blocks:
   64.71.137.241, from 64.71.137.241, 3w1d ago
      Route metric is 0, traffic share count is 1
      AS Hops 2
      Route tag 6939
      MPLS label: none
route-views>show bgp 217.197.228.106
BGP routing table entry for 217.197.224.0/20, version 1034417018
Paths: (24 available, best #22, table default)
  Not advertised to any peer
  Refresh Epoch 1
  7018 1299 20485 24739
    12.0.1.63 from 12.0.1.63 (12.0.1.63)
      Origin IGP, localpref 100, valid, external
      Community: 7018:5000 7018:37232
      path 7FE14BBC6190 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  701 1273 3216 24739
    137.39.3.55 from 137.39.3.55 (137.39.3.55)
      Origin IGP, localpref 100, valid, external
      path 7FE0AD28FA20 RPKI State valid
      rx pathid: 0, tx pathid: 0 ```


2.```
vagrant@vagrant:~/devops-netology$ sudo ip link add name dum0 type dummy
vagrant@vagrant:~/devops-netology$ sudo ip link set dum0 up
vagrant@vagrant:~/devops-netology$ sudo ip addr add 10.0.0.100/32 dev dum0
 sudo ip route add 10.0.0.100 via 10.0.2.2
vagrant@vagrant:~/devops-netology$ ip route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
10.0.0.100 via 10.0.2.2 dev eth0
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
```
3-4.
```

vagrant@vagrant:~/devops-netology$ ss -t -a

State        Recv-Q       Send-Q              Local Address:Port                 Peer Address:Port        Process
LISTEN       0            4096                      0.0.0.0:sunrpc                    0.0.0.0:*
LISTEN       0            4096                127.0.0.53%lo:domain                    0.0.0.0:*
LISTEN       0            128                       0.0.0.0:ssh                       0.0.0.0:*
ESTAB        0            0                       10.0.2.15:ssh                      10.0.2.2:49841
LISTEN       0            4096                         [::]:sunrpc                       [::]:*
LISTEN       0            128                          [::]:ssh                          [::]:*
vagrant@vagrant:~/devops-netology$ ss -u -a
State        Recv-Q       Send-Q               Local Address:Port                 Peer Address:Port       Process
UNCONN       0            0                    127.0.0.53%lo:domain                    0.0.0.0:*
UNCONN       0            0                   10.0.2.15%eth0:bootpc                    0.0.0.0:*
UNCONN       0            0                          0.0.0.0:sunrpc                    0.0.0.0:*
UNCONN       0            0                             [::]:sunrpc                       [::]:* ```

