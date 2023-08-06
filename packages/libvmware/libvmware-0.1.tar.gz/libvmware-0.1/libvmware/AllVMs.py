from __future__ import print_function
from pyVmomi import vim, vmodl
import vCenterConnect


def __store_vm_info(vm):
    summary = vm.summary
    info = {
        'name': summary.config.name,
        'template': summary.config.template,
        'path': summary.config.vmPathName,
        'guest': summary.config.guestFullName,
        'instance uuid': summary.config.instanceUuid,
        'bios uuid': summary.config.uuid,
        'state': summary.runtime.powerState
    }

    if summary.config.annotation:
        info.update({'annotation': summary.config.annotation})

    if summary.guest is not None:
        info.update(
            {
                'vmware tools': summary.guest.toolsStatus,
                'ip': summary.guest.ipAddress
            }
        )

    if summary.runtime.question is not None:
        info.update({'question': summary.runtime.question.text})

    return info

def get_all():
    try:
        si = vCenterConnect.connect()
        content = si.RetrieveContent()
        container = content.rootFolder
        view_type = [vim.VirtualMachine]
        recursive = True
        container_view = content.viewManager.CreateContainerView(
            container,
            view_type,
            recursive
        )

        vms = container_view.view
        vm_data = []
        for vm in vms:
            vm_data.append(__store_vm_info(vm))

        return vm_data

    except vmodl.MethodFault as error:
        print('Caught vmodl fault: {}'.format(error.msg))
