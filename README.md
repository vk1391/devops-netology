1. - текст Dockerfile манифеста
```
FROM centos:7
RUN yum update -y && yum install wget nano sudo -y
RUN groupadd elasticsearch && useradd -g elasticsearch elasticsearch && usermod -a -G wheel elasticsearch
RUN mkdir /var/lib/logs \
    && chown elasticsearch:elasticsearch /var/lib/logs \
    && mkdir /var/lib/data \
    && chown elasticsearch:elasticsearch /var/lib/data
RUN su elasticsearch
RUN yum install java-11-openjdk perl-Digest-SHA -y  
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.0-linux-x86_64.tar.gz
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.0-linux-x86_64.tar.gz.sha512
RUN shasum -a 512 -c elasticsearch-7.17.0-linux-x86_64.tar.gz.sha512 
RUN tar -xzf elasticsearch-7.17.0-linux-x86_64.tar.gz
RUN cd elasticsearch-7.17.0/
ADD elasticsearch.yml /elasticsearch-7.17.0/config/
RUN sudo chown -R elasticsearch:elasticsearch /elasticsearch-7.17.0     
USER elasticsearch
ENV ES_JAVA_HOME=/usr/
ENV ES_HOME=/elasticsearch-7.17.0
CMD ["/bin/elasticsearch"]
```
   - ссылку на образ в репозитории dockerhub
```
https://hub.docker.com/repository/docker/f6987c8d6ed5/elastik5
```
   - ответ elasticsearch на запрос пути / в json виде
```
curl 172.17.0.2:9200 -o out2.json
"name" : "master",
  "cluster_name" : "netology-test",
  "cluster_uuid" : "vVtUTuaSQx-ip5ILuFd34A",
  "version" : {
    "number" : "7.17.0",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "bee86328705acaa9a6daede7140defd4d9ec56bd",
    "build_date" : "2022-01-28T08:36:04.875279988Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
```


2. - добавил, заполнил 3 индекса
```
[elasticsearch@eadb2749e7bd /]$ curl -X PUT '172.17.0.2:9200:9200/ind-1' -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-1"}[elasticsearch@eadb2749e7bd /]$
[elasticsearch@eadb2749e7bd /]$ curl -X PUT 172.17.0.2:9200:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-2"}[elasticsearch@eadb2749e7bd /]$ read escape sequence
vagrant@vagrant:~/elastik$ curl -X PUT 172.17.0.2:9200:9200/ind-3 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-3"}vagrant@vagrant:~/elastik$
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases F5WW_Rx5Qda_sxL17ETNNA   1   0         42            0     38.9mb         38.9mb
green  open   ind-1            uKf6hdrnSuWpOAbWWwUF9Q   1   0          0            0       226b           226b
yellow open   ind-3            uncmpQxIQxaB4NMbT8NGmg   4   2          0            0       904b           904b
yellow open   ind-2            U9p4-glyRwKZBj6Rs-P-3A   2   1          0            0       452b           452b
```
    - информация по индексам,кластеру
```
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cluster/health/ind-1?pretty'
{
  "cluster_name" : "netology-test",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1,
  "active_shards" : 1,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cluster/health/ind-2?pretty'
{
  "cluster_name" : "netology-test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 2,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 2,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cluster/health/ind-3?pretty'
{
  "cluster_name" : "netology-test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 4,
  "active_shards" : 4,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 8,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cluster/health/?pretty'
{
  "cluster_name" : "netology-test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 10,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cluster/health/?pretty=true'
{
  "cluster_name" : "netology-test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 10,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```
   - удалил индексы
```
vagrant@vagrant:~/elastik$ curl -X DELETE '172.17.0.2:9200/ind-1?pretty'
{
  "acknowledged" : true
}
vagrant@vagrant:~/elastik$ curl -X DELETE '172.17.0.2:9200/ind-2?pretty'
{
  "acknowledged" : true
}
vagrant@vagrant:~/elastik$ curl -X DELETE '172.17.0.2:9200/ind-3?pretty'
{
  "acknowledged" : true
```
   - почему статус жёлтый?
   - Ответ: Статус жёлтый так как индексам указаны реплики а их пока нет так как одна нода.

3. - Запрос API и результат вызова API для создания репозитория
```
curl -X POST 172.17.0.2:9200/_snapshot/netology_backup?pretty -H 'Content-Type: application/json' -d'{"type": "fs", "settings": { "location":"/elastikbackup/snapshots" }}'
{
 "acknowledged" : true
}
vagrant@vagrant:~/elastik$ curl -X GET 172.17.0.2:9200/_snapshot/netology_backup?pretty
{
 "netology_backup" : {
   "type" : "fs",
   "settings" : {
     "location" : "/elastikbackup/snapshots"
   }
 }
}
```
   - создание индекса,его бекап
   
```
vagrant@vagrant:~/elastik$ curl -X PUT 172.17.0.2:9200/test -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"test"}vagrant@vagrant:~/elastik$
vagrant@vagrant:~/elastik$ curl -X GET 172.17.0.2:9200/test/?pretty
{
 "test" : {
   "aliases" : { },
   "mappings" : { },
   "settings" : {
     "index" : {
       "routing" : {
         "allocation" : {
           "include" : {
             "_tier_preference" : "data_content"
           }
         }
       },
       "number_of_shards" : "1",
       "provided_name" : "test",
       "creation_date" : "1644263702795",
       "number_of_replicas" : "0",
       "uuid" : "N1RmRpUHQLOofa5A0t-DFw",
       "version" : {
         "created" : "7170099"
       }
     }
   }
 }
}
vagrant@vagrant:~/elastik$ curl -X PUT 172.17.0.2:9200/_snapshot/netology_backup/elasticsearch?wait_for_completion=true
{"snapshot":{"snapshot":"elasticsearch","uuid":"VdPHdKeBSsGEdWZ2KyIUkA","repository":"netology_backup","version_id":7170099,"version":"7.17.0","indices":[".geoip_databases",".ds-ilm-history-5-2022.02.07-000
001",".ds-.logs-deprecation.elasticsearch-default-2022.02.07-000001","test"],"data_streams":["ilm-history-5",".logs-deprecation.elasticsearch-default"],"include_global_state":true,"state":"SUCCESS","start_t
ime":"2022-02-07T19:58:13.989Z","start_time_in_millis":1644263893989,"end_time":"2022-02-07T19:58:15.394Z","end_time_in_millis":1644263895394,"duration_in_millis":1405,"failures":[],"shards":{"total":4,"fai
led":0,"successful":4},"feature_states":[{"feature_name":"geoip","indices":[".geoip_databases"]}]}}

vagrant@vagrant:~/elastik$
vagrant@vagrant:~/elastik$
vagrant@vagrant:~/elastik$ docker attach eadb2749e7bd
[elasticsearch@eadb2749e7bd /]$ cd elastikbackup/
[elasticsearch@eadb2749e7bd elastikbackup]$ cd snapshots/
[elasticsearch@eadb2749e7bd snapshots]$ ll
total 48
-rw-rw-r-- 1 elasticsearch elasticsearch  1425 Feb  7 19:58 index-0
-rw-rw-r-- 1 elasticsearch elasticsearch     8 Feb  7 19:58 index.latest
drwxrwxr-x 6 elasticsearch elasticsearch  4096 Feb  7 19:58 indices
-rw-rw-r-- 1 elasticsearch elasticsearch 29282 Feb  7 19:58 meta-VdPHdKeBSsGEdWZ2KyIUkA.dat
-rw-rw-r-- 1 elasticsearch elasticsearch   712 Feb  7 19:58 snap-VdPHdKeBSsGEdWZ2KyIUkA.dat
```
   - удаление индекса,создание нового, востановление из бекапа
```
vagrant@vagrant:~/elastik$ curl -X DELETE '172.17.0.2:9200/test?pretty'
{
 "acknowledged" : true
}
vagrant@vagrant:~/elastik$ curl -X PUT 172.17.0.2:9200/test-2?pretty -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{
 "acknowledged" : true,
 "shards_acknowledged" : true,
 "index" : "test-2"
 curl -X POST 172.17.0.2:9200/_snapshot/netology_backup/elasticsearch/_restore?pretty -H 'Content-Type: application/json' -d'{"include_global_state":true, "indices":"*,-.*"}'
vagrant@vagrant:~/elastik$ curl -X GET '172.17.0.2:9200/_cat/indices?v'
vagrant@vagrant:~/elastik$ curl -X GET 172.17.0.2:9200/_cat/indices?v
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2           InRDdwINRjetQt_D9exezw   1   0          0            0       226b           226b
green  open   test             N1RmRpUHQLOofa5A0t-DFw   1   0          0            0       226b           226b
```
