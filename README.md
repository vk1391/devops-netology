1. chdir("/tmp")

2. Я так понимаю сначала обращается к /lib/x86_64-linux-gnu/libmagic.so.1" в котором указаны пути к бд. В итоге обращается к openat "/etc/magic" и "/usr/share/misc/magic.mgc"
3. обнулить содержимое дескриптора файла я полагаю

4. Да.Пока дочерний процесс не вернёт код возврата он останиться висеть в таблице процессов,занимаю ресурсы CPU

5. Если я правильно понял задание,то: 
	sudo /usr/sbin/opensnoop-bpfcc -d 1
	PID    COMM               FD ERR PATH
	798    vminfo              6   0 /var/run/utmp
	587    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
	587    dbus-daemon        19   0 /usr/share/dbus-1/system-services
	587    dbus-daemon        -1   2 /lib/dbus-1/system-services
	587    dbus-daemon        19   0 /var/lib/snapd/dbus-1/system-services/
6. uname использует системный вызов uname. в мануале на debian ни слова не сказано о том откуда uname подтягивает информацию  и почему то нет второго мануала.в мануале с rhel:
	65:       Part of the utsname information is also accessible  via  /proc/sys/ker
	66-       nel/ostype, hostname, osrelease, version, domainname.

7.в мануале баша написано: command1  command2
	command2 is executed if, and only if, command1 returns an exit status of zero (success).
	соответвенно если первая команда не вернет exit 0 то тогда вторая и не начнёт отрабатывать.

	; - знак последовательного разделения команд,второй команде всеравно,как отработала первая

	set -e вернёт exit (0)если вернется не нулевое значение exit последней выполненной команды,что приминительно к данному примеру позволит выполнить вторую команду так как первая по 	окончанию вернёт exit(0)(set -e test -d /tmp/some_dir  echo Hi)

8. -e Немедленный выход, если команда завершается с ненулевым статусом.
	-u Обрабатывать неустановленные переменные как ошибку при подстановке
	-x Печатать команды и их аргументы по мере их выполнения.
	-o pipefail сли вышеуказанные команды завершились успешно,то возвращается exit(0),если нет то 1
	нужно для того что бы понимать что происходит во время скрипта и контролировать его выполнение на каждом этапе.
9. У меня в основном S(процесс ожидает (т.е. спит менее 20 секунд)) и I(процесс в приоритетном режиме бездействует (т.е. спит больше 20 секунд))

