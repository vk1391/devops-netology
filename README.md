2. нет не могут, так как ссылка и файл имеют один и тот же айнод, соответвенно и права будут одинаковыми.

	vagrant@vagrant:~/test$ touch 111

	vagrant@vagrant:~/test$ ln 111 test111

	vagrant@vagrant:~/test$ ls -ali

	total 16

	131576 drwxrwxr-x 2 vagrant vagrant  4096 Aug 27 12:36 .

	131074 drwxr-xr-x 9 vagrant vagrant 12288 Aug 27 12:35 ..

	131577 -rw-rw-r-- 2 vagrant vagrant     0 Aug 27 12:35 111

	131577 -rw-rw-r-- 2 vagrant vagrant     0 Aug 27 12:35 test111

3. готово
	vagrant@vagrant:~$ lsblk
	NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
	sda                    8:0    0   64G  0 disk
	sda1                 8:1    0  512M  0 part /boot/efi
	sda2                 8:2    0    1K  0 part
	sda5                 8:5    0 63.5G  0 part
	vgvagrant-root   253:0    0 62.6G  0 lvm  /
	 vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
	sdb                    8:16   0  2.5G  0 disk
	sdc                    8:32   0  2.5G  0 disk

5.  sudo sfdisk -d /dev/sdb > partittions.txt
	vagrant@vagrant:~$ sudo sfdisk /dev/sdc <partittions.txt
	Checking that no-one is using this disk right now ... OK

	Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
	Disk model: VBOX HARDDISK
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes

	>>> Script header accepted.
	>>> Script header accepted.
	>>> Script header accepted.
	>>> Script header accepted.
	>>> Created a new DOS disklabel with disk identifier 0x3b32236f.
	/dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
	/dev/sdc2: Created a new partition 2 of type 'Linux' and of size 511 MiB.
	/dev/sdc3: Done.

	New situation:
	Disklabel type: dos
	Disk identifier: 0x3b32236f

	Device     Boot   Start     End Sectors  Size Id Type
	/dev/sdc1          2048 4196351 4194304    2G 83 Linux
	/dev/sdc2       4196352 5242879 1046528  511M 83 Linux

	The partition table has been altered.
	Calling ioctl() to re-read partition table.
	Syncing disks.
	vagrant@vagrant:~$ lsblk
	NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
	sda                    8:0    0   64G  0 disk
	sda1                 8:1    0  512M  0 part /boot/efi
	sda2                 8:2    0    1K  0 part
	sda5                 8:5    0 63.5G  0 part
	  vgvagrant-root   253:0    0 62.6G  0 lvm  /
	  vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
	sdb                    8:16   0  2.5G  0 disk
	sdb1                 8:17   0    2G  0 part
	sdb2                 8:18   0  511M  0 part
	sdc                    8:32   0  2.5G  0 disk
	sdc1                 8:33   0    2G  0 part
	sdc2                 8:34   0  511M  0 part.

6.  sudo mdadm --create --verbose /dev/md1 -l 1 -n 2 /dev/sd{b1,c1}
	mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
	mdadm: size set to 2094080K
	Continue creating array? y
	mdadm: Defaulting to version 1.2 metadata
	mdadm: array /dev/md1 started.
	vagrant@vagrant:~$ lsblk
	NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
	sda                    8:0    0   64G  0 disk
	sda1                 8:1    0  512M  0 part  /boot/efi
	sda2                 8:2    0    1K  0 part
	sda5                 8:5    0 63.5G  0 part
	  vgvagrant-root   253:0    0 62.6G  0 lvm   /
	  vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
	sdb                    8:16   0  2.5G  0 disk
	sdb1                 8:17   0    2G  0 part
	 md1                9:1    0    2G  0 raid1
	sdb2                 8:18   0  511M  0 part
	sdc                    8:32   0  2.5G  0 disk
	sdc1                 8:33   0    2G  0 part
	 md1                9:1    0    2G  0 raid1
	sdc2                 8:34   0  511M  0 part

7. sudo mdadm --create --verbose /dev/md0 -l 0 -n 2 /dev/sd{b2,c2}

	lsblk
	NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
	sda                    8:0    0   64G  0 disk
	sda1                 8:1    0  512M  0 part  /boot/efi
	sda2                 8:2    0    1K  0 part
	sda5                 8:5    0 63.5G  0 part
	  vgvagrant-root   253:0    0 62.6G  0 lvm   /
	  vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
	sdb                    8:16   0  2.5G  0 disk
	sdb1                 8:17   0    2G  0 part
	 md1                9:1    0    2G  0 raid1
	sdb2                 8:18   0  511M  0 part
	  md0                9:0    0 1018M  0 raid0
	sdc                    8:32   0  2.5G  0 disk
	sdc1                 8:33   0    2G  0 part
	 md1                9:1    0    2G  0 raid1
	sdc2                 8:34   0  511M  0 part
	  md0                9:0    0 1018M  0 raid0

8. vagrant@vagrant:~$ sudo pvcreate /dev/md1
  
	Physical volume "/dev/md1" successfully created.
	
	vagrant@vagrant:~$ sudo pvcreate /dev/md0

	Physical volume "/dev/md0" successfully created.

9. sudo vgcreate vg1 /dev/md1 /dev/md0

10. sudo lvcreate -L 100M vg1 /dev/md0

	vagrant@vagrant:~$ lsblk
	NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
	sda                    8:0    0   64G  0 disk
	sda1                 8:1    0  512M  0 part  /boot/efi
	sda2                 8:2    0    1K  0 part
	sda5                 8:5    0 63.5G  0 part
	  vgvagrant-root   253:0    0 62.6G  0 lvm   /
	  vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
	sdb                    8:16   0  2.5G  0 disk
	sdb1                 8:17   0    2G  0 part
	 md1                9:1    0    2G  0 raid1
	sdb2                 8:18   0  511M  0 part
	  md0                9:0    0 1018M  0 raid0
	    vg1-lvol0      253:2    0  100M  0 lvm
	sdc                    8:32   0  2.5G  0 disk
	sdc1                 8:33   0    2G  0 part
	 md1                9:1    0    2G  0 raid1
	sdc2                 8:34   0  511M  0 part
	  md0                9:0    0 1018M  0 raid0
	    vg1-lvol0      253:2    0  100M  0 lvm

11. sudo mkfs.ext4 /dev/vg1/lvol0
	
	mke2fs 1.45.5 (07-Jan-2020)
	
	Creating filesystem with 25600 4k blocks and 25600 inodes


	Allocating group tables: done

	Writing inode tables: done

	Creating journal (1024 blocks): done

	Writing superblocks and filesystem accounting information: done

14-15. gzip -t /tmp/new/test.gz

	vagrant@vagrant:/tmp/new$ echo $?
	
	0
	lsblk
	NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT

	sda                    8:0    0   64G  0 disk
	
	sda1                 8:1    0  512M  0 part  /boot/efi

	sda2                 8:2    0    1K  0 part
	
	sda5                 8:5    0 63.5G  0 part
	
	  vgvagrant-root   253:0    0 62.6G  0 lvm   /

	vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
	sdb                    8:16   0  2.5G  0 disk
	
	sdb1                 8:17   0    2G  0 part
	 md126              9:126  0    2G  0 raid1
	
	sdb2                 8:18   0  511M  0 part

	  md127              9:127  0 1018M  0 raid0

	    vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new
	
	sdc                    8:32   0  2.5G  0 disk

	sdc1                 8:33   0    2G  0 part

	 md126              9:126  0    2G  0 raid1
	
	sdc2                 8:34   0  511M  0 part
	  md127              9:127  0 1018M  0 raid0
	    vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new

16. sudo pvmove /dev/md127 /dev/md126
  
	/dev/md127: Moved: 20.00%
	
	/dev/md127: Moved: 100.00%

vagrant@vagrant:/tmp/new$ lsblk

NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk
sda1                 8:1    0  512M  0 part  /boot/efi
sda2                 8:2    0    1K  0 part
sda5                 8:5    0 63.5G  0 part
  vgvagrant-root   253:0    0 62.6G  0 lvm   /
  vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk
sdb1                 8:17   0    2G  0 part
 md126              9:126  0    2G  0 raid1
   vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new
sdb2                 8:18   0  511M  0 part
  md127              9:127  0 1018M  0 raid0
sdc                    8:32   0  2.5G  0 disk
sdc1                 8:33   0    2G  0 part
 md126              9:126  0    2G  0 raid1
   vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new
sdc2                 8:34   0  511M  0 part
  md127              9:127  0 1018M  0 raid0	

17. sudo mdadm /dev/md126 --fail /dev/sdb1

	mdadm: set /dev/sdb1 faulty in /dev/md126

18. dmesg |grep md126

[    3.317390] md/raid1:md126: active with 2 out of 2 mirrors

[    3.317415] md126: detected capacity change from 0 to 2144337920

[ 1593.085251] md/raid1:md126: Disk failure on sdb1, disabling device.

               md/raid1:md126: Operation continuing on 1 devices.

19. Доступен.
	gzip -t /tmp/new/test.gz
	vagrant@vagrant:/tmp/new$ echo $?
	0
