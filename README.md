1.с первым разобрался
2
```.
#!/usr/bin/env python3
import os

bash_command = ["cd /home/vagrant/devops-netology", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(("/home/vagrant/devops-netology/"),(prepare_result))
```
3.
```
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
```

4.
```
додумался только до этого

#!/usr/bin/env python3

import os

bash_command = ["dig google.com | grep google.com. ","dig drive.google.com | grep google.com.","dig mail.google.com | grep google.com" ]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('ANSWER SECTION') != 0:
        prepare_result = result.replace('\tANSWER SECTION   ', '')
        print(prepare_result)
```
