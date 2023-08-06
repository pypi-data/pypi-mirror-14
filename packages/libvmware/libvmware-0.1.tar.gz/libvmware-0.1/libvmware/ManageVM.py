from pyVmomi import vim
import vCenterConnect
import Tasks
import requests


class ManageVM:
    def __init__(self, vm_name=None, uuid=None, ip_address=None, vm_user=None, vm_pwd=None):
        self.vm_name = vm_name
        self.uuid = uuid
        self.ip_address = ip_address
        self.vm_user = vm_user
        self.vm_pwd = vm_pwd
        self.si = vCenterConnect.connect()
        self.vm = None
        if self.vm_name:
            self.vm = self.si.content.searchIndex.FindByDnsName(None, self.vm_name, True)

        elif self.uuid:
            self.vm = self.si.content.searchIndex.FindByUuid(None, self.uuid, True, True)

        elif self.ip_address:
            self.vm = self.si.content.searchIndex.FindByIp(None, self.ip_address, True)

        if self.vm is None:
            raise SystemExit('Unable to find specified VM or no VM ID given')

    def reboot(self):
        task = self.vm.ResetVM_Task()
        Tasks.wait_for_tasks(self.si, [task])

        return '{} Rebooted'.format(self.vm)

    def power_off(self):
        task = self.vm.PowerOffVM_Task()
        Tasks.wait_for_tasks(self.si, [task])

        return '{} Shutdown'.format(self.vm)

    def power_on(self):
        task = self.vm.PowerOnVM_Task()
        Tasks.wait_for_tasks(self.si, [task])

        return '{} Powered on'.format(self.vm)

    def run_command(self, cmd, args):
        content = self.si.RetrieveContent()
        creds = vim.vm.guest.NamePasswordAuthentication(
            username=self.vm_user,
            password=self.vm_pwd
        )

        try:
            pm = content.guestOperationsManager.processManager
            ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath=cmd,
                arguments=args
            )
            res = pm.StartProgramInGuest(self.vm, creds, ps)

            return 'Program Started/Run'

        except IOError as e:
            return e

    def upload_file(self, file, dest):
        content = self.si.RetrieveContent
        creds = vim.vm.guest.NamePasswordAuthentication(
            username=self.vm_user,
            password=self.vm_pwd
        )

        with open(file, 'rb') as f:
            file_contents = f.read()

        try:
            file_attribute = vim.vm.guest.FileManager.FileAttributes()
            url = content.guestOperationsManager.filemanager. \
                InitiateFileTransferToGuest(
                self.vm,
                creds,
                dest,
                file_attribute,
                len(file_contents),
                True
            )

            resp = requests.put(url, data=file_contents, verify=False)

            if not resp.status_code == 200:
                return 0

            else:
                return 'Successfully Uploaded File'

        except IOError as e:
            return e

    def create_snapshot(self, snapshot_name, description=None):
        if description is None:
            task = self.vm.CreateSnapshot_Task(
                name=snapshot_name,
                memory=True,
                quiesce=False
            )

        else:
            task = self.vm.CreateSnapshot_Task(
                name=snapshot_name,
                description=description,
                memory=True,
                quiesce=False
            )
        snap_info = self.vm.snapshot

        tree = snap_info.rootSnapshotList
        while tree[0].childSnapshotList is not None:
            if len(tree[0].childSnapshotList) < 1:
                break
            tree = tree[0].childSnapshotList

            return (tree[0].name, tree[0].discription)

    def destroy(self):
        if format(self.vm.runtime.powerState) == 'poweredOn':
            self.power_off()

        task = self.vm.Destroy_Task()
        Tasks.wait_for_tasks(self.si, [task])

        return '{} Destroyed'.format(self.vm)
