1. так как :"whereis cd
cd:"
прихожу к выводу что это не отдельная программа.Нашёл описание cd в мануале bash,
так что походе что cd это команда bash для смены дериктории

5. vagrant@vagrant:~$ echo "blablabla" >1
vagrant@vagrant:~$ cat <1 >2
vagrant@vagrant:~$ cat 2
blablabla

6. думаю пока в окно эмулятора не переключюсь не увижу

10. 226 строка /proc/<PID>/cmdline содержит полный путь до процесса если процесс не зомби
279 строка /proc/[pid]/exe символическая ссылка с фвктическим путем к исполняемому файлу

12. Я так понимаю потомцу что подключившись по SSH я уже подключился к системе по PTS, по этому пишет что не TTY
ключ -t выделяет новое PTS.мануал по SSH пишет следующее:"Принудительное выделение псевдотерминала. 
Это можно использовать для выполнения произвольных экранных программ на удаленном компьютере,
 что может быть очень полезно, например при реализации услуг меню. 
Несколько параметров -t принудительно выделяют tty, даже если ssh не имеет локального tty"  
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:wSHl+h4vAtTT7mbkj2lbGyxWXWTUf6VUliwpncjwLPM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
vagrant@localhost's password:
Permission denied, please try again.
vagrant@localhost's password:
not a tty
vagrant@vagrant:~$ ssh localhost -t 'tty'
vagrant@localhost's password:
/dev/pts/2
Connection to localhost closed.

