from __future__ import print_function
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl
from Config import settings
from libvmware import vCenterConnect


class Clone:
    def __init__(self, template, vm_name):
        self.local_settings = settings
        self.local_settings.update(
            {
                'template': template,
                'vm name': vm_name,
                'power on': True,
                'datacenter name': None,
                'datastore name': None,
                'vm folder': None,
                'cluster name': None,
                'resource pool': None
            }
        )

    def __wait_for_task(self, task):
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                print('There was an error')
                task_done = True

    def __get_obj(self, content, vimtype, name):
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)

        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break
        return obj

    def __clone(
            self, content, template, vm_name, si, datacenter_name, vm_folder,
            datastore_name, cluster_name, resource_pool, power_on
    ):
        datacenter = self.__get_obj(content, [vim.Datacenter], datacenter_name)

        if vm_folder:
            dest_folder = self.__get_obj(content, [vim.Folder], vm_folder)
        else:
            dest_folder = datacenter.vmFolder

        if datastore_name:
            datastore = self.__get_obj(content, [vim.Datastore], datastore_name)
        else:
            datastore = self.__get_obj(
                content,
                [vim.Datastore],
                template.datastore[0].info.name
            )

        cluster = self.__get_obj(content, [vim.ClusterComputeResource], cluster_name)

        if resource_pool:
            resource_pool = self.__get_obj(content, [vim.ResourcePool], resource_pool)
        else:
            resource_pool = cluster.resourcePool

        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = power_on

        task = template.Clone(
            folder=dest_folder,
            name=vm_name,
            spec=clonespec
        )
        self.__wait_for_task(task)

    def create(self):
        si = vCenterConnect.connect()
        content = si.RetrieveContent()
        template = None
        template = self.__get_obj(content, [vim.VirtualMachine], self.local_settings['template'])

        if template:
            self.__clone(
                content,
                template,
                self.local_settings['vm name'],
                si,
                self.local_settings['datacenter name'],
                self.local_settings['vm folder'],
                self.local_settings['datastore name'],
                self.local_settings['cluster name'],
                self.local_settings['resource pool'],
                self.local_settings['power on']
            )

        else:
            print('template not found...')
