#!/usr/bin/env python3
import socket
import json
import yaml
path="/home/vagrant/dir1/"
i=1
host = 'mail.google.com'
host2 = 'google.com'
host3 = 'drive.google.com'
ip1 = socket.gethostbyname(host)
ip2 = socket.gethostbyname(host2)
ip3 = socket.gethostbyname(host3)
d = {host: ip1, host2: ip2, host3: ip3}
while 1==1:
    i+=1
    if i == 3:
      break
    for x in d:
      ipnew=socket.gethostbyname(x)
      if ipnew == d[x]:
        print ('MATCH', x, d[x], ipnew)
      else :
        print ('ERROR', x, d[x], ipnew)

      with open(path+x+".json",'w') as j:
        json_data= json.dumps({x:ipnew})
        j.write(json_data)
      with open(path+x+".yml",'w') as y:
        yaml_data= yaml.dump([{x:ipnew}])
        y.write(yaml_data)
