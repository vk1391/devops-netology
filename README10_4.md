1.  Вам необходимо поднять в докере:

   - elasticsearch(hot и warm ноды)
   - logstash
   - kibana
   - filebeat
   
   и связать их между собой.

  - Logstash следует сконфигурировать для приёма по tcp json сообщений.

  - Filebeat следует сконфигурировать для отправки логов docker вашей системы в logstash.

  В директории help находится манифест docker-compose и конфигурации filebeat/logstash для быстрого выполнения данного задания.

  Результатом выполнения данного задания должны быть:

  скриншот docker ps через 5 минут после старта всех контейнеров (их должно быть 5)
  скриншот интерфейса kibana
  docker-compose манифест (если вы не использовали директорию help)
  ваши yml конфигурации для стека (если вы не использовали директорию help
Ответ:
docker-compose
```
 Max virtual memory areas vm.max_map_count must be least 262144
# sysctl -w vm.max_map_count=262144

version: '2.2'
services:

  es-hot:
    image: elasticsearch:7.16.2
    container_name: es-hot
    environment:
      - node.name=es-hot
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es-warm
      - cluster.initial_master_nodes=es-hot,es-warm
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - data01:/usr/share/elasticsearch/data:Z
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
    networks:
      - elastic
    depends_on:
      - es-warm

  es-warm:
    image: elasticsearch:7.16.2
    container_name: es-warm
    environment:
      - node.name=es-warm
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es-hot
      - cluster.initial_master_nodes=es-hot,es-warm
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - data02:/usr/share/elasticsearch/data:Z
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    networks:
      - elastic

  kibana:
    image: kibana:7.16.2
    container_name: kibana
    ports:
      - 5601:5601
    environment:
      ELASTICSEARCH_URL: http://es-hot:9200
      ELASTICSEARCH_HOSTS: '["http://es-hot:9200","http://es-warm:9200"]'
    networks:
      - elastic
    depends_on:
      - es-hot
      - es-warm

  logstash:
    image: "docker.elastic.co/logstash/logstash:7.16.2"
    container_name: logstash
    ports:
      - 5046:5046
    volumes:
      - ./configs/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      - ./configs/logstash.yml:/usr/share/logstash/config/logstash.yml
    networks:
      - elastic
    depends_on:
      - es-hot
      - es-warm

  filebeat:     
    image: elastic/filebeat:7.16.2
    container_name: filebeat
    privileged: true
    user: root
    volumes:
      - ./configs/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker:/var/lib/docker:ro
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - logstash
    networks:
      - elastic

  some_application:
    image: library/python:3.9-alpine
    container_name: some_app
    volumes:
      - ./pinger/run.py:/opt/run.py:Z
    entrypoint: python3 /opt/run.py

volumes:
  data01:
    driver: local
  data02:
    driver: local
  data03:
    driver: local

networks:
  elastic:
    driver: bridge
```

logstash.conf
```
input {
    beats {
    port => 5046
    codec => json
  }
}

filter {
    json {
        source =>  "message"
    }
    
  
  mutate {
    add_field => { "FieldName" => "MyField6" }
  }
}

output {
  elasticsearch { 
    hosts => ["es-hot:9200"] 
    index => "logstash-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

filebeat.yaml
```
filebeat.inputs:
  - type: container
    enabled: true
    paths:
      - '/var/lib/docker/containers/*/*.log'
    json.keys_under_root: true
#    document_type: docker
  
processors:
  - add_docker_metadata:
      host: "unix:///var/run/docker.sock"
  - decode_json_fields:
      fields: ["message"]
      target: ""
      overwrite_keys: true
  - add_docker_metadata: ~

filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false
  
output.logstash:
  hosts: ["logstash:5046"]

#output.console:
#  enabled: true

logging.json: true
logging.metrics.enabled: false
```
2.Перейдите в меню создания index-patterns в kibana и создайте несколько index-patterns из имеющихся.

Перейдите в меню просмотра логов в kibana (Discover) и самостоятельно изучите как отображаются логи и как производить поиск по логам.

В манифесте директории help также приведенно dummy приложение, которое генерирует рандомные события в stdout контейнера. 
Данные логи должны порождать индекс logstash-* в elasticsearch. 
Если данного индекса нет - воспользуйтесь советами и источниками из раздела "Дополнительные ссылки" данного ДЗ.
Ответ:
![Иллюстрация к проекту](https://github.com/vk1391/devops-netology/blob/db9bf93edd42d1eccee51225b9dd5c882f96d83d/ELK_fin.jpg)
