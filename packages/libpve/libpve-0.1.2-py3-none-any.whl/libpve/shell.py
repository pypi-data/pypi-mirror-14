# -*- coding: utf-8 -*-

import os
import paramiko
import sys

class Shell:

    hostname = None
    last_id = None
    next_id = None
    ssh = None

    def __init__(self, verbose=False):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property
    def next_id(self):
        """Holds the next free vmid.

        Returns:
            int: vmid

        """
        return int(self.run('get /cluster/nextid').strip().strip('"'))

    def add_to_pool(self, pool_id, pve_vmid_list):
        """Adds virtual machines to a pool.

        Returns:
            str: Output of the command.

        """
        cmd = 'set /pools/{}'.format(pool_id)
        cmd += ' -vms {}'.format(pve_vmid_list)
        return self.run(cmd)

    def create(self, technology, profile={}, vmid=None, node=None):
        """Creates a new virtual machine.

        Returns:
            str: Output of the command.

        """
        if(technology == 'lxc'):
            ostemplate = profile['ostemplate']
        if(node == None):
            node = self.hostname
        if(vmid == None):
            vmid = self.next_id

        self.last_id = vmid
        cmd = 'create /nodes/{}/{}'.format(node, technology)
        cmd += ' -ostemplate {}'.format(ostemplate)
        cmd += ' -vmid {}'.format(vmid)
        return self.run(cmd)

    def create_template(self, technology, vmid, node=None):
        """Creates a new template.

        Returns:
            str: Output of the command.

        """
        if(node == None):
            node = self.hostname

        self.last_id = vmid
        cmd = 'create /nodes/{}/{}/{}/template'.format(node, technology, vmid)
        return self.run(cmd)

    def remove_from_pool(self, pool_id, pve_vmid_list):
        """Removes virtual machines from pool.

        Returns:
            str: Output of the command.

        """
        cmd = 'set /pools/{}'.format(pool_id)
        cmd += ' -vms {}'.format(pve_vmid_list)
        cmd += ' -delete True'
        return self.run(cmd)

    def destroy(self, technology, vmid, node=None):
        """Destroys a virtual machine.

        Returns:
            str: Output of the command.

        """
        if(node == None):
            node = self.hostname

        self.last_id = vmid
        cmd = 'delete /nodes/{}/{}/{}'.format(node, technology, vmid)
        return self.run(cmd)

    def run(self, cmd, silent=False):
        """Runs a command on the node.

        Returns:
            str: Output of the command.

        """
        if(silent!=True):
            print('SHELL: {}'.format(cmd))
        try:
            stdin, stdout, stderr = self.ssh.exec_command('pvesh {}'.format(cmd))
            if self.stderr.read() != b'' and silent != True:
                print(self.stderr.read().decode(), file=sys.stderr)
        except Exception as E:
            self.ssh.disconnect()
            print(E)
        finally:
            return stdout.read().decode()

    def connect(self, fqdn, port=22, username='root', password=None):
        """Connects to a node.

        Returns:
            str: Output of the command.

        """
        self.ssh.connect(fqdn, port, username, password, allow_agent=False)
        self.hostname = fqdn.split('.')[0]

    def disconnect(self):
        """Disconnects from a node.

        """
        self.ssh.close()

    def start(self, technology, vmid, node=None):
        """Starts a container.

        Returns:
            str: Output of the command.

        """
        if(node == None):
            node = self.hostname

        self.last_id = vmid
        cmd = 'create /nodes/{}/{}/{}/status/start'.format(node, technology, vmid)
        return self.run(cmd)

    def stop(self, technology, vmid, node=None):
        """Stops a container.

        Returns:
            str: Output of the command.

        """
        if(node == None):
            node = self.hostname

        self.last_id = vmid
        cmd = 'create /nodes/{}/{}/{}/status/stop'.format(node, technology, vmid)
        return self.run(cmd)

