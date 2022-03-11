2.  - 1. Packer
    - 2.
 - main.tf
```terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "0.68.0"
    }
  }
}

provider "yandex" {
token = 
cloud_id                 = "b1g8v8m7g8l57ts5j64b"
folder_id                = "b1g95kjdui4sc1hk937i"
zone                     = "ru-central1-a"

resource "yandex_compute_instance" "node01" {
name                      = "node01"
zone                      = "ru-central1-a"
hostname                  = "node01.netology.cloud"
allow_stopping_for_update = true

resources {
  cores  = 8
  memory = 8
  }

  boot_disk {
    initialize_params {
      image_id    = "fd80le4b8gt2u33lvubr"
      name        = "root-node01"
      type        = "network-nvme"
      size        = "50"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.default.id}"
    nat       = "true"
  }

  metadata = {
    ssh-keys = "user-data = "${file("~/terr2/meta.txt")}"
  }
}
resource "yandex_vpc_network" "default" {
  name = "net"
}

resource "yandex_vpc_subnet" "default" {
  name = "subnet"
  zone       = "ru-central1-a"
  network_id = "${yandex_vpc_network.foo.id}"
  v4_cidr_blocks = ["192.168.101.0/24"]
}
```


 - meta.txt
```
users:
  - name: vagrant
    groups: wheel
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh-authorized-keys:
      - ssh-rsa AAAAB3NzaC
```

 - otput.tf
```
output "internal_ip_address_node01_yandex_cloud" {
  value = yandex_compute_instance.node01.network_interface.0.ip_address
}

output "external_ip_address_node01_yandex_cloud" {
  value = yandex_compute_instance.node01.network_interface.0.nat_ip_address
}
```
