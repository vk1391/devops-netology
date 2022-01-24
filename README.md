
1. - Docker-compose файл
``` 
version: '3.9'

services:
    mysql:
        image: mysql:latest
        container_name: mysql
        volumes:
            - ./mysqldb:/var/lib/mysql
        environment:
            - MYSQL_ROOT_PASSWORD=1234
        expose:
            - '3306'
```
```
mysql> \s;
--------------
mysql  Ver 8.0.27-0ubuntu0.20.04.1 for Linux on x86_64 ((Ubuntu))

Connection id:          14
Current database:       test
Current user:           root@172.18.0.1
SSL:                    Cipher in use is TLS_AES_256_GCM_SHA384
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         8.0.28 MySQL Community Server - GPL
Protocol version:       10
Connection:             172.18.0.2 via TCP/IP
Server characterset:    utf8mb4
Db     characterset:    utf8mb4
Client characterset:    utf8mb4
Conn.  characterset:    utf8mb4
TCP port:               3306
Binary data as:         Hexadecimal
Uptime:                 30 min 41 sec

Threads: 3  Questions: 66  Slow queries: 0  Opens: 168  Flush tables: 3  Open ta
bles: 86  Queries per second avg: 0.035
--------------
mysql> use test
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| orders         |
+----------------+
1 row in set (0.00 sec)
mysql> select count(*) from orders where price >300;
+----------+
| count(*) |
+----------+
|        1 |
+----------+
1 row in set (0.01 sec)
```
2.
``` 
mysql> CREATE USER 'test'@'localhost' IDENTIFIED BY 'test-pass';
Query OK, 0 rows affected (0.04 sec)

mysql> ALTER USER 'test'@'localhost'
    -> IDENTIFIED BY 'test-pass'
    -> WITH
    -> MAX_QUERIES_PER_HOUR 100
    -> PASSWORD EXPIRE INTERVAL 180 DAY
    -> FAILED_LOGIN_ATTEMPTS 3;
Query OK, 0 rows affected (0.01 sec)

mysql>  ALTER USER 'test'@'localhost' ATTRIBUTE '{"fname":"James", "lname":"Pret
ty"}';
Query OK, 0 rows affected (0.01 sec)
GRANT Select ON test.orders TO 'test'@'localhost';
Query OK, 0 rows affected, 1 warning (0.01 sec)
SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER='test';
+------+-----------+---------------------------------------+
| USER | HOST      | ATTRIBUTE                             |
+------+-----------+---------------------------------------+
| test | localhost | {"fname": "James", "lname": "Pretty"} |
+------+-----------+---------------------------------------+
1 row in set (0.01 sec)
```
3.
``` 
mysql> SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> SELECT TABLE_NAME,ENGINE,ROW_FORMAT,TABLE_ROWS,DATA_LENGTH,INDEX_LENGTH FROM information_schema.TABLES WHERE table_name = 'orders' and  TABLE_SCHEMA = 'test' ORDER BY ENGINE asc;
+------------+--------+------------+------------+-------------+--------------+
| TABLE_NAME | ENGINE | ROW_FORMAT | TABLE_ROWS | DATA_LENGTH | INDEX_LENGTH |
+------------+--------+------------+------------+-------------+--------------+
| orders     | InnoDB | Dynamic    |          5 |       16384 |            0 |
+------------+--------+------------+------------+-------------+--------------+
1 row in set (0.00 sec)

mysql> SHOW PROFILES;
+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                                                                                                             |
+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        1 | 0.00223750 | SELECT TABLE_NAME,ENGINE,ROW_FORMAT,TABLE_ROWS,DATA_LENGTH,INDEX_LENGTH FROM information_schema.TABLES WHERE table_name = 'orders' and  TABLE_SCHEMA = 'test' ORDER BY ENGINE asc |
+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> ALTER TABLE orders ENGINE = MyISAM;
Query OK, 5 rows affected (0.11 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> ALTER TABLE orders ENGINE = InnoDB;
Query OK, 5 rows affected (0.15 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SHOW PROFILES;
+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                                                                                                             |
+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        1 | 0.00223750 | SELECT TABLE_NAME,ENGINE,ROW_FORMAT,TABLE_ROWS,DATA_LENGTH,INDEX_LENGTH FROM information_schema.TABLES WHERE table_name = 'orders' and  TABLE_SCHEMA = 'test' ORDER BY ENGINE asc |
|        2 | 0.10595800 | ALTER TABLE orders ENGINE = MyISAM                                                                                                                                                |
|        3 | 0.15031900 | ALTER TABLE orders ENGINE = InnoDB                                                                                                                                                |
+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 1 warning (0.00 sec)
```
4.
```
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

 Custom config should go here
!includedir /etc/mysql/conf.d/
innodb_flush_log_at_trx_commit = 2
innodb_log_buffer_size = 1M
key_buffer_size = 615M 
max_binlog_size	= 100M
```
