```

2.version: "3.9"

networks:
  postgres:
    driver: bridge

volumes:
    data: {}
    backup: {}
    backup_res: {}

services:

  postgre:
    image: postgres:12.9
    environment:
      POSTGRES_DB: "test_db"
      POSTGRES_USER: "test-admin-user"
      POSTGRES_PASSWORD: "12345678"
      PGDATA: "/var/lib/postgresql/data/pgdata"
    container_name: postgre_main
    volumes:
      - ./data:/var/lib/pgsql/data
      - ./backup:/backup
    restart: always
    networks:
      - postgres
    ports:
      - "5432:5432"

  postgre_res:
    image: postgres:12.9
    environment:
      POSTGRES_DB: "test_db"
      POSTGRES_USER: "test-admin-user"
      POSTGRES_PASSWORD: "12345678"
      PGDATA: "/var/lib/postgresql/data/pgdata"
      container_name: postgre_res
    volumes:
      - ./backup_res:/backup
    restart: always
    networks:
      - postgres
#    ports:
#      - "5432:5432"

test_db=# \l
                                             List of databases
   Name    |      Owner      | Encoding |  Collate   |   Ctype    |            Access privileges
-----------+-----------------+----------+------------+------------+-----------------------------------------
 postgres  | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"test-admin-user"                   +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
 template1 | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"test-admin-user"                   +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
 test_db   | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/"test-admin-user"                  +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
(4 rows)

test_db=# \d
             List of relations
 Schema |  Name   | Type  |      Owner
--------+---------+-------+-----------------
 public | clients | table | test-admin-user
 public | order   | table | test-admin-user
(2 rows)

test_db=# \du
                                       List of roles
    Role name     |                         Attributes                         | Member of
------------------+------------------------------------------------------------+-----------
 test-admin-user  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 test-simple-user | No inheritance                                             | {}

3.insert into public."order" VALUES (1, 'Chocolade', 10), (2, 'Printer', 3000), (3, 'Book', 500), (4, 'monitor', 7000), (5, 'Guitar', 4000);
  insert into public."clients" VALUES (1, 'Ivanov I I', 'USA'), (2, 'Petrov P P', 'Canada'), (3, 'Bach I S', 'Japan'),
  (4, 'Dio R J', 'Russia'), (5, 'Ritchie Blackmore', 'Russia');
  test_db=# select count (*) from public."order";
   count
  -------
       5
  (1 row)


  test_db=# select count (*) from public."clients";
   count
  -------
       5
  (1 row)

4. update  public."clients" set indent = 3 where id = 1;
   update  public."clients" set indent = 4 where id = 2;
   update  public."clients" set indent = 5 where id = 3;

5. explain select * from public."clients" where indent is not null
6.pg_dump -h 172.22.0.3 -U test-admin-user test_db > ~/postgres/test_db1
psql -h 172.22.0.2 -U test-admin-user test_db < ~/postgres/test_db1
psql -h 172.22.0.2 -U test-admin-user test_db
Password for user test-admin-user:
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1))
Type "help" for help.

test_db=# \d
             List of relations
 Schema |  Name   | Type  |      Owner
--------+---------+-------+-----------------
 public | clients | table | test-admin-user
 public | order   | table | test-admin-user
(2 rows)

```
