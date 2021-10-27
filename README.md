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
питон вариант

```
import socket
i=1
host = 'mail.google.com'
host2 = 'google.com'
host3 = 'drive.google.com'
ip1 = socket.gethostbyname(host)
ip2 = socket.gethostbyname(host2)
ip3 = socket.gethostbyname(host3)
d = {host: ip1, host2: ip2, host3: ip3}
while 1==1:
    for x in d:
      ipnew=socket.gethostbyname(x)
      if ipnew == d[x] and i==1:
        print ('MATCH', x, d[x], ipnew)
      else :
        print ('ERROR', x, d[x], ipnew)
    i+=1
    if i == 5: 
      break
```
