#!/usr/bin/env python3

import libpve

pve = libpve.Shell()
pve.connect('proxmox')
output = pve.create('lxc', profile={"ostemplate": "local:vztmpl/ubuntu-14.04-standard_14.04-1_amd64.tar.gz"})
print(output)
output = pve.add_to_pool('pool2', pve.last_id)
print(output)
output = pve.start('lxc', pve.last_id)
print(output)
output = pve.stop('lxc', pve.last_id)
print(output)
output = pve.destroy('lxc', pve.last_id)
print(output)
