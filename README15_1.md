# Домашнее задание к занятию "15.1. Организация сети"

Домашнее задание будет состоять из обязательной части, которую необходимо выполнить на провайдере Яндекс.Облако и дополнительной части в AWS по желанию. Все домашние задания в 15 блоке связаны друг с другом и в конце представляют пример законченной инфраструктуры.  
Все задания требуется выполнить с помощью Terraform, результатом выполненного домашнего задания будет код в репозитории. 

Перед началом работ следует настроить доступ до облачных ресурсов из Terraform используя материалы прошлых лекций и [ДЗ](https://github.com/netology-code/virt-homeworks/tree/master/07-terraform-02-syntax ). А также заранее выбрать регион (в случае AWS) и зону.

---
## Задание 1. Яндекс.Облако (обязательное к выполнению)

1. Создать VPC.
- Создать пустую VPC. Выбрать зону.
2. Публичная подсеть.
- Создать в vpc subnet с названием public, сетью 192.168.10.0/24.
- Создать в этой подсети NAT-инстанс, присвоив ему адрес 192.168.10.254. В качестве image_id использовать fd80mrhj8fl2oe87o4e1
- Создать в этой публичной подсети виртуалку с публичным IP и подключиться к ней, убедиться что есть доступ к интернету.
3. Приватная подсеть.
- Создать в vpc subnet с названием private, сетью 192.168.20.0/24.
- Создать route table. Добавить статический маршрут, направляющий весь исходящий трафик private сети в NAT-инстанс
- Создать в этой приватной подсети виртуалку с внутренним IP, подключиться к ней через виртуалку, созданную ранее и убедиться что есть доступ к интернету

## Решение:

- [main.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/main.tf)
- [nat-ins.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/nat-ins.tf)
- [vpc.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/vpc.tf)
- [subnet.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/subnet.tf)
- [route-table.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/route-table.tf)
- [machines.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/machines.tf)
- [outputs.tf](https://github.com/vk1391/devops-netology/blob/cde1fd434ac546c9158ae50220e1dcf2e804d2ae/terraform/outputs.tf)

## Проверка:
```
vagrant@vagrant:~$ yc compute instances list --folder-id b1g95kjdui4sc1hk937i
+----------------------+--------------+---------------+---------+----------------+----------------+
|          ID          |     NAME     |    ZONE ID    | STATUS  |  EXTERNAL IP   |  INTERNAL IP   |
+----------------------+--------------+---------------+---------+----------------+----------------+
| fhmdto8pte61hj99ocjl | nat-instance | ru-central1-a | RUNNING | 37.120.212.212 | 192.168.10.254 |
| fhmpji1mjn8uf8dvab79 | vm-public    | ru-central1-a | RUNNING | 51.250.75.150  | 192.168.10.8   |
| fhmrimtiq336mdogut6i | vm-private   | ru-central1-a | RUNNING |                | 192.168.20.33  |
+----------------------+--------------+---------------+---------+----------------+----------------+

vagrant@vagrant:~$ ssh ubuntu@51.250.75.150 curl -sS ifconfig.me
51.250.75.150

vagrant@vagrant:~$ ssh -J ubuntu@51.250.75.151 ubuntu@192.168.20.33 curl -sS ifconfig.me
37.120.212.212
