# Домашнее задание к занятию "14.5 SecurityContext, NetworkPolicies"

## Задача 1: Рассмотрите пример 14.5/example-security-context.yml

Создайте модуль

```
kubectl apply -f 14.5/example-security-context.yml
```

Проверьте установленные настройки внутри контейнера

```
kubectl logs security-context-demo
uid=1000 gid=3000 groups=3000
```
![Иллюстрация к проекту](https://github.com/vk1391/devops-netology/blob/8af3f35ccd46f8d17b5cf2f40488aa8714164448/netology%2014.5.jpg))
