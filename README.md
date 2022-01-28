1.  - Docker-compose файл:
```
version: '3.9'
volumes:
  data: {}
services:
  db:
    image: postgres:13.5
    restart: always
    environment:
      POSTGRES_DB: "test_database"
      POSTGRES_PASSWORD: "1234"
      PGDATA: "/var/lib/postgresql/data/pgdata"
      POSTGRES_USER: "test"

    container_name: postgre
    volumes:
      - ./data://var/lib/postgresql/data/pgdata"
    ports:
      - "5432:5432"
  postgres=# \l
                                     List of databases
           Name      | Owner | Encoding |  Collate   |   Ctype    | Access privileges
      ---------------+-------+----------+------------+------------+-------------------
       postgres      | test  | UTF8     | en_US.utf8 | en_US.utf8 |
       template0     | test  | UTF8     | en_US.utf8 | en_US.utf8 | =c/test          +
                     |       |          |            |            | test=CTc/test
       template1     | test  | UTF8     | en_US.utf8 | en_US.utf8 | =c/test          +
                     |       |          |            |            | test=CTc/test
       test_database | test  | UTF8     | en_US.utf8 | en_US.utf8 |
      (4 rows)

\c название базы - переключение на другую бд

\dt перечень таблиц в базе

 \dS+ наименование таблицы базы - описание содержимого таблиц

 \q выход из сессии pgsql
 ```
 2. - востановил бекап а базу 
```
psql -h 172.19.0.2 -U test test_database < ~/postgres/test_dump.sql
```
  - analyze
  ```
 test_database=# analyze verbose orders;
 INFO:  analyzing "public.orders"
 INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
 ANALYZE
 ```
  - найдите столбец таблицы orders с наибольшим средним значением размера элементов в байтах:
  ```
 test_database=# select attname,avg_width from pg_stats where tablename='orders' ORDER BY abs(pg_stats.avg_width) DESC;
  attname | avg_width
 ---------+-----------
  title   |        16
  id      |         4
  price   |         4
 (3 rows)
 ```
3. - надо было сразу делать партиционирование и правила фильтрации
```
alter table orders rename to orders_old;
ALTER TABLE
test_database=# create table orders (id integer, title varchar(80), price integer) partition by range(price);
CREATE TABLE
test_database=# create table orders_1 partition of orders for values from (0) to (499);
CREATE TABLE
test_database=# create table orders_2 partition of orders for values from (499) to (999999999);
CREATE TABLE
test_database=# insert into orders (id, title, price) select * from orders_old;

test_database=# select * from orders_1;

 id |        title         | price
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
(4 rows)

test_database=# select * from orders_2;
 id |       title        | price
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  7 | Me and my bash-pet |   499
  8 | Dbiezdmin          |   501
(4 rows)
```
4. - так как убунта 20 у меня пришлось обновить psql client до 13.5 версии
```
pg_dump -h 172.19.0.2 -U test test_database > ~/postgres/new.psql.testdump

