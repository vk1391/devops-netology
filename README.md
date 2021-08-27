(1).	[Unit]


	Description=Node_exporter

	After=multi-user.target

	[Service]

	Type=idle

	ExecStart=/home/vagrant/node_exporter-1.2.2.linux-amd64/node_exporter -f $EXTRA_OPTS

	[Install]

	WantedBy=multi-user.target



(4). сделав dmesg -H 
	DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
	CPU MTRRs all blank - virtualized system.
	Hypervisor detected: KVM не понятно какой kvm???
        я думаю осознаёт.

(5). fs.nr_open = 1048576 - максимальное значение открытых дескрипторов,соответвует строке open files в ulinit -aH.

(6). "Ubuntu / Canonical решили показать ошибку. Debian решил предоставить тот же вывод как для ps -aux, так и ps aux.
	 В общем, довольно запутанно.
	 Но, как сказано: это / должно было сделать скрипты совместимыми.
	 И вы можете использовать то, что вам нравится."
	 Так и я из под рута заходил, так что разночтений быть не должно.

	вроде как вышло,с командой sleep почему то дважды отработала.
   
	1754 pts/2    00:00:00 sleep

	vagrant@vagrant:~$ sudo nsenter --target 1754 --pid --mount
	
	root@vagrant:/# ps -aux
	
	USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
	
	root           1  0.0  0.4   9836  4020 pts/2    S+   12:00   0:00 /bin/bash
	
	root          10  0.0  0.0   8076   592 pts/2    T    12:00   0:00 sleep 1h
	
	root          34  0.0  0.0   8076   592 pts/2    S    12:07   0:00 sleep 1h
	
	root          40  0.0  0.3   9836  3900 pts/1    S    12:10   0:00 -bash
	
	root          49  0.0  0.3  11680  3616 pts/1    R+   12:10   0:00 ps -aux

(7). как написано на одном сайте ,это бинарная бомба.Процесс пораждающий два новых процесс и так далее.
	В принцыпе можно ограничить кол-во процессов до приемлемого и жить с этим.
	dmesg регулирует следующим образом:
	fork rejected by pids controller in /user.slice/user-1000.slice/session-6.scope

