1. Опишите основные плюсы и минусы pull и push систем мониторинга.
Ответ:

- PUSH - удобна для использования в динамически создаваемых машинах (например из докер-контейнеров), 
       так как в противном случае Система мониторинга должна будет узнавать о новых хостах для их опроса,
       можно задавать глубину мониторинга именно на машинах, добавление новых иснтансов автоматом добавит метрику без настройки системы мониторинга
       Передача данных в открытом виде по сети, при наличии ПД в метриках есть риск утечки данных
       так же есть риск потери данных при недоступности системы мониторинга (принимающей метрики)
       передаваться данные должны на один ресурс для сбора (одну систему мониторинга) одним источником
- PULL - контроль над метриками с единой точки, возможность конеккта по SSL к агентам.
       более высокий уровень контроля за источниками метрик ,т.е. всегда известно кто откуда что передает,
       возможность ставить в Downtime (отключение алертинга) целых систем без потери передаваемых данных (хотя думаю в Push так же реализуемо)
       Ну и то что разными системами мониторинга можно получать одни и теже метрики, можно выподнять запросы метрики с изменяемой переодичностью 
       так же запрашивать метрики в ручном режиме в обход систем сбора 
       минус - неудобство для динамических машин (докер-контейнеры) нужно динамически собирать статистику о наличии машин, нужен дополнительный оркестратор
2. Какие из ниже перечисленных систем относятся к push модели, а какие к pull? А может есть гибридные?
 - Prometheus	PULL : одновременно опрашивает системы, так же может получать данные от агентов exporter-ов, и получать метрики о событиях
 - TICK	PUSH : telegraph передает информацию в систему хранилище, так же данные получает Kapasitor по Pull модели
 - Zabbix	PULL : использует подключение к ресурсом по стандартным протоколам или же оправшивает сови агенты у становленные на серверах для получения данных
 - VictoriaMetrics	БОльше подходит PUSH, так как метрики записываются в нее, но это (если правильно понял по описанию) система для хранения по большей части, и получает данные, которые к нейпишут другие системы
 - Nagios	PULL : Так же использует опрос snmp, агентов, которые собирают информацию
3.
```
vagrant@tick:~/sandbox$ curl http://localhost:8086/ping -v
*   Trying ::1:8086...
* TCP_NODELAY set
* Connected to localhost (::1) port 8086 (#0)
> GET /ping HTTP/1.1
> Host: localhost:8086
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 204 No Content
< Content-Type: application/json
< Request-Id: 78ad5474-f490-11ec-813e-0242c0a82003
< X-Influxdb-Build: OSS
< X-Influxdb-Version: 1.8.10
< X-Request-Id: 78ad5474-f490-11ec-813e-0242c0a82003
< Date: Sat, 25 Jun 2022 14:09:47 GMT
< 
* Connection #0 to host localhost left intact
```

```
vagrant@tick:~/sandbox$ curl http://localhost:8888 -v
*   Trying ::1:8888...
* TCP_NODELAY set
* Connected to localhost (::1) port 8888 (#0)
> GET / HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Cache-Control: public, max-age=3600
< Content-Length: 336
< Content-Security-Policy: script-src 'self'; object-src 'self'
< Content-Type: text/html; charset=utf-8
< Etag: "3362220244"
< Last-Modified: Tue, 22 Mar 2022 20:02:44 GMT
< Vary: Accept-Encoding
< X-Chronograf-Version: 1.9.4
< X-Content-Type-Options: nosniff
< X-Frame-Options: SAMEORIGIN
< X-Xss-Protection: 1; mode=block
< Date: Sat, 25 Jun 2022 14:14:21 GMT
< 
* Connection #0 to host localhost left intact
```

```
vagrant@tick:~/sandbox$ curl http://localhost:9092/kapacitor/v1/ping -v
*   Trying ::1:9092...
* TCP_NODELAY set
* Connected to localhost (::1) port 9092 (#0)
> GET /kapacitor/v1/ping HTTP/1.1
> Host: localhost:9092
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 204 No Content
< Content-Type: application/json; charset=utf-8
< Request-Id: 3779c7f3-f491-11ec-8142-000000000000
< X-Kapacitor-Version: 1.6.4
< Date: Sat, 25 Jun 2022 14:15:07 GMT
< 
* Connection #0 to host localhost left intact
```
4.  Перейдите в веб-интерфейс Chronograf (http://localhost:8888) и откройте вкладку Data explorer.

Нажмите на кнопку Add a query
Изучите вывод интерфейса и выберите БД telegraf.autogen
В measurments выберите mem->host->telegraf_container_id , а в fields выберите used_percent. Внизу появится график утилизации оперативной памяти в контейнере telegraf.
Вверху вы можете увидеть запрос, аналогичный SQL-синтаксису. Поэкспериментируйте с запросом, попробуйте изменить группировку и интервал наблюдений.
Для выполнения задания приведите скриншот с отображением метрик утилизации места на диске (disk->host->telegraf_container_id) из веб-интерфейса.
Ответ:
![Иллюстрация к проекту](https://github.com/vk1391/devops-netology/blob/31bd9b1fa26ee0b92dc6551d68154b90bcfda96e/2.jpg)
5.  ![Иллюстрация к проекту](https://github.com/vk1391/devops-netology/blob/31bd9b1fa26ee0b92dc6551d68154b90bcfda96e/3.jpg)
