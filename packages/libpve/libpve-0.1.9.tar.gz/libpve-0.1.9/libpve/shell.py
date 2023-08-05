# -*- coding: utf-8 -*-

import paramiko
import sys

class Shell:

    hostname = None
    last_id = None
    next_id = None
    ssh = None
    verbose = None

    def __init__(self, verbose=False):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.verbose = verbose

    @property
    def next_id(self):
        """Holds the next free vmid.

        Returns:
            int: vmid

        """
        return int(self.run('get /cluster/nextid'))

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
        if(node == None):
            node = self.hostname
        if(vmid == None):
            vmid = self.next_id

        self.last_id = vmid

        # Magic cmd creation
        cmd = 'create /nodes/{}/{}'.format(node, technology)

        # ostemplate
        if(technology == 'lxc'):
            cmd += ' -ostemplate {}'.format(profile['ostemplate'])
            del profile['ostemplate']
        else:
            print('{} is not yet supported'.format(technology))
            self.disconnect(1)

        # vmid
        cmd += ' -vmid {}'.format(vmid)

        # description, if available - need to be in exclamation mark for whitespace
        if('description' in profile.keys()):
            cmd += ' -description \'{}\''.format(profile['description'])
            del profile['description']

        # rest of the profile
        for parameter, value in profile.items():
            cmd += ' -{} {}'.format(parameter, value)
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

    def run(self, cmd):
        """Runs a command on the node.

        Returns:
            str: Output of the command.

        """
        if(self.verbose == True):
            print('SHELL: {}'.format(cmd))
        try:
            stdin, stdout, stderr = self.ssh.exec_command('pvesh {}'.format(cmd))
        except Exception as E:
            print(E)
            self.disconnect(1)
        else:
            error = stderr.read().decode().strip()
            if(self.verbose == True and error != ''):
                if(error!='200 OK'):
                    print('ERROR: {}'.format(error))
                    self.disconnect(1)
            output = stdout.read().decode().strip().strip('"')
            if(self.verbose == True and output != ''):
                print('RETURN: {}'.format(output))
            return output

    def connect(self, fqdn, port=22, username='root', password=None):
        """Connects to a node.

        Returns:
            str: Output of the command.

        """
        self.ssh.connect(fqdn, port, username, password, allow_agent=False)
        self.hostname = fqdn.split('.')[0]

    def disconnect(self, return_status=0):
        """Disconnects from a node.

        """
        self.ssh.close()
        sys.exit(return_status)

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

