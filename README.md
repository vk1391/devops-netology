1. Попробуйте запустить playbook на окружении из test.yml, зафиксируйте какое значение имеет факт some_fact для указанного хоста при выполнении playbook'a.
Ответ:я так понимаю - 12.
```
vagrant@vagrant:~/ansble$ ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] ************************************************************

TASK [Gathering Facts] ***********************************************************
ok: [localhost]

TASK [Print OS] ******************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ****************************************************************
ok: [localhost] => {
    "msg": 12
}
```
2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
Ответ:
```
group_vars/all/examp.yml
```
3. Воспользуйтесь подготовленным (используется docker) или создайте собственное окружение для проведения дальнейших испытаний.
Ответ:
```
vagrant@vagrant:~/ansble$ docker ps
CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS         PORTS     NAMES
6b97b9c01c7e   688353a31fde   "/bin/bash"   2 seconds ago   Up 1 second              centos7
98113114bd1f   f7596bdb3fd6   "bash"        2 minutes ago   Up 2 minutes             ubuntu
```
4.Проведите запуск playbook на окружении из prod.yml. Зафиксируйте полученные значения some_fact для каждого из managed host.
Ответ:
```
vagrant@vagrant:~/ansble$ ansible-playbook site.yml -i inventory/prod.yml

PLAY [Print os facts] ****************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **********************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Debian"
}

TASK [Print fact] ********************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}

PLAY RECAP ***************************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
5-6. Добавьте факты в group_vars каждой из групп хостов так, чтобы для some_fact получились следующие значения: для deb - 'deb default fact', для el - 'el default fact'.
Повторите запуск playbook на окружении prod.yml. Убедитесь, что выдаются корректные значения для всех хостов.
Ответ:
```
vagrant@vagrant:~/ansble$ ansible-playbook site.yml -i inventory/prod.yml

PLAY [Print os facts] ****************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **********************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Debian"
}

TASK [Print fact] ********************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ***************************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
9. Посмотрите при помощи ansible-doc список плагинов для подключения. Выберите подходящий для работы на control node
Ответ:
Local
```
vagrant@vagrant:~/ansble$ ansible-doc -t connection -F
[WARNING]: Collection ibm.qradar does not support Ansible version 2.12.3
[WARNING]: Collection frr.frr does not support Ansible version 2.12.3
[WARNING]: Collection splunk.es does not support Ansible version 2.12.3
ansible.netcommon.httpapi      /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/ansible/netcommon/plugins/connection/httpapi.py
ansible.netcommon.libssh       /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/ansible/netcommon/plugins/connection/libssh.py
ansible.netcommon.napalm       /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/ansible/netcommon/plugins/connection/napalm.py
ansible.netcommon.netconf      /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/ansible/netcommon/plugins/connection/netconf.py
ansible.netcommon.network_cli  /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/ansible/netcommon/plugins/connection/network_cli.py
ansible.netcommon.persistent   /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/ansible/netcommon/plugins/connection/persistent.py
community.aws.aws_ssm          /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/aws/plugins/connection/aws_ssm.py
community.docker.docker        /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/docker/plugins/connection/docker.py
community.docker.docker_api    /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/docker/plugins/connection/docker_api.py
community.docker.nsenter       /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/docker/plugins/connection/nsenter.py
community.general.chroot       /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/chroot.py
community.general.funcd        /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/funcd.py
community.general.iocage       /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/iocage.py
community.general.jail         /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/jail.py
community.general.lxc          /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/lxc.py
community.general.lxd          /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/lxd.py
community.general.qubes        /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/qubes.py
community.general.saltstack    /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/saltstack.py
community.general.zone         /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/general/plugins/connection/zone.py
community.libvirt.libvirt_lxc  /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/libvirt/plugins/connection/libvirt_lxc.py
community.libvirt.libvirt_qemu /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/libvirt/plugins/connection/libvirt_qemu.py
community.okd.oc               /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/okd/plugins/connection/oc.py
community.vmware.vmware_tools  /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/community/vmware/plugins/connection/vmware_tools.py
containers.podman.buildah      /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/containers/podman/plugins/connection/buildah.py
containers.podman.podman       /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/containers/podman/plugins/connection/podman.py
kubernetes.core.kubectl        /home/vagrant/.local/lib/python3.8/site-packages/ansible_collections/kubernetes/core/plugins/connection/kubectl.py
local                          /home/vagrant/.local/lib/python3.8/site-packages/ansible/plugins/connection/local.py
paramiko_ssh                   /home/vagrant/.local/lib/python3.8/site-packages/ansible/plugins/connection/paramiko_ssh.py
psrp                           /home/vagrant/.local/lib/python3.8/site-packages/ansible/plugins/connection/psrp.py
ssh                            /home/vagrant/.local/lib/python3.8/site-packages/ansible/plugins/connection/ssh.py
winrm                          /home/vagrant/.local/lib/python3.8/site-packages/ansible/plugins/connection/winrm.py
```
10-11. В prod.yml добавьте новую группу хостов с именем local, в ней разместите localhost с необходимым типом подключения.
Запустите playbook на окружении prod.yml. При запуске ansible должен запросить у вас пароль. Убедитесь что факты some_fact для каждого из хостов определены из верных group_vars
Ответ: 
```vagrant@vagrant:~/ansble$ ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password:

PLAY [Print os facts] ****************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************************
ok: [Localhost]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **********************************************************************************************************************************************************************************************
ok: [Localhost] => {
    "msg": "Ubuntu"
}
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Debian"
}

TASK [Print fact] ********************************************************************************************************************************************************************************************
ok: [Localhost] => {
    "msg": 12
}
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ***************************************************************************************************************************************************************************************************
Localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
