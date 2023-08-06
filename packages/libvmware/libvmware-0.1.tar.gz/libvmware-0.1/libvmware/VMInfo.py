from __future__ import print_function
import vCenterConnect


class VMInfo:
    def __init__(self):
        self.details = {}

    def get_all_info(self, vm_name):
        si = vCenterConnect.connect()

        search_index = si.content.searchIndex

        vm = search_index.FindByDnsName(
            None,
            vm_name,
            True
        )

        if vm is None:
            print('Could not find {}'.format(vm_name))

        self.details.update(
            {
                'name': vm.summary.config.name,
                'UUID': vm.summary.config.instanceUuid,
                'path to vm': vm.summary.config.vmPathName,
                'guest OS ID': vm.summary.config.guestId,
                'guest os Name': vm.summary.config.guestFullName,
                'host name': vm.runtime.host.name
            }
        )

        if vm.summary.guest is not None:
            self.details.update({'ip address': vm.summary.guest.ipAddress})

        return self.details

    def get_ip(self, vm_name):
        info = self.get_all_info(vm_name)
        ip = info['ip address']

        return ip