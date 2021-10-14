1.
```
а. c=a+b - bash не видит здесь переменных, вывел как текст.
б. 1+2 здесь bash определил наличие переменных и выполнил подстановку,но вывел как текст так как не увидел ссылки на арифметическое действие
в. 3 здесь и выполнил подстановку и арефметическое действие
```

2.
```
while ((1==1)); do curl https://localhost:4757; if(($? !=0)); then date >> curl.log; fi; done;

```

3.
```
 cat curlip
#!/usr/bin/env bash
ip=(192.168.0.1 173.194.222.113 87.250.250.242)
for i in {1..5}
do
    for a in ${ip[@]}
    do
        curl $a
        echo $a status=$? >>log
    done
done

vagrant@vagrant:~/devops-netology$ cat log
192.168.0.1 status=7
173.194.222.113 status=0
87.250.250.242 status=0
192.168.0.1 status=7
173.194.222.113 status=0
87.250.250.242 status=0
192.168.0.1 status=7
173.194.222.113 status=0
87.250.250.242 status=0
192.168.0.1 status=7
173.194.222.113 status=0
87.250.250.242 status=0
192.168.0.1 status=7
173.194.222.113 status=0
87.250.250.242 status=0
```

4.
```
#!/usr/bin/env bash
ip=(192.168.0.1 173.194.222.113 87.250.250.242)
t=0
while (($t == 0))
do
date >>log2
    for a in ${ip[@]}
    do
        curl $a
        t=$?
        if (($t != 0))
        then
                echo "Destination host unreacheble!!!!" $a status=$t >>log2
        fi
    done
done

vagrant@vagrant:~/devops-netology$ cat log2
Thu 14 Oct 2021 02:26:09 PM UTC
Destination host unreacheble!!!! 192.168.0.1 status=7
Thu 14 Oct 2021 02:26:12 PM UTC
Destination host unreacheble!!!! 192.168.0.1 status=7
Thu 14 Oct 2021 02:26:14 PM UTC
Destination host unreacheble!!!! 192.168.0.1 status=7
Thu 14 Oct 2021 02:26:17 PM UTC

```
