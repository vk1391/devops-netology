1.  https://hub.docker.com/repository/docker/f6987c8d6ed5/nginx2

2.  Из всех перечисленных вариантов я б использовал докер на этапе разработки 
в первых трёх случаях.В продакшн бы на докере не вывел.Что касается системам мониторинга,то для 
не критичных систем можно реализовать,весь вопрос в вычислительных мощностях сервера,если использовать 
разные хостовые машины для ELK и prometheus и Grafana то возможно.

3.  ```vagrant@vagrant:~$ docker exec -it ecc703f857d8 touch /data/file1
vagrant@vagrant:~$ pwd
vagrant@vagrant:~/data$ touch file2
vagrant@vagrant:~/data$ ll
total 8
drwxrwxr-x 2 vagrant vagrant 4096 Dec 21 19:12 ./
drwxr-xr-x 6 vagrant vagrant 4096 Dec 21 18:38 ../
-rw-r--r-- 1 root    root       0 Dec 21 19:12 file1
-rw-rw-r-- 1 vagrant vagrant    0 Dec 21 19:12 file2
vagrant@vagrant:~/data$ docker ps
CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS         PORTS     NAMES
836169bb57fe   6f4986d78878   "bash"        4 minutes ago   Up 4 minutes             debian
ecc703f857d8   5d0da3dc9764   "/bin/bash"   7 minutes ago   Up 7 minutes             centos
vagrant@vagrant:~/data$ docker attach 836169bb57fe
root@836169bb57fe:/# ls -al /data
total 8
drwxrwxr-x 2 1000 1000 4096 Dec 21 19:12 .
drwxr-xr-x 1 root root 4096 Dec 21 19:08 ..
-rw-r--r-- 1 root root    0 Dec 21 19:12 file1
-rw-rw-r-- 1 1000 1000    0 Dec 21 19:12 file2
```
