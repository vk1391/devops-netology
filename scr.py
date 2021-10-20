#!/usr/bin/env python3
import os

path = str(input('название директории: '))
bash_command = ["cd " +path,"git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(("/home/vagrant/devops-netology/"),(prepare_result))

