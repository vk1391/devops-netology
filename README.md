1.```
   yandex: Complete!
==> yandex: Stopping instance...
==> yandex: Deleting instance...
    yandex: Instance has been deleted!
==> yandex: Creating image: centos-7-base
==> yandex: Waiting for image to complete...
==> yandex: Success image create...
==> yandex: Destroying boot disk...
    yandex: Disk has been deleted!
Build 'yandex' finished after 1 minute 53 seconds.

==> Wait completed after 1 minute 53 seconds

==> Builds finished. The artifacts of successful builds are:
--> yandex: A disk image was created: centos-7-base (id: fd80lsjo4sl8l5kc44u5) with family name centos
vagrant@vagrant:~$ yc compute image list
+----------------------+---------------+--------+----------------------+--------+
|          ID          |     NAME      | FAMILY |     PRODUCT IDS      | STATUS |
+----------------------+---------------+--------+----------------------+--------+
| fd80lsjo4sl8l5kc44u5 | centos-7-base | centos | f2eaujc3c3g545cncg0v | READY  |
+----------------------+---------------+--------+----------------------+--------+
```

