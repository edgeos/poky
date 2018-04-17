"""
Function to set MAC address of a VM using pyVmomi.
Based of this pyVmomi sample:
https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/change_vm_nic_state.py
"""
from .tasks import wait_for_tasks
from pyVmomi import vim


def set_mac_address(service_instance, vm, mac_address):
    """Set MAC address for VM with given vm_name, using given service_instance
    for ESXi server. Assumes network adapter is "Network Adapter 1"
    :param service_instance: Service Instance for ESXi server
    :param vm: VM object corresponding to VM to set MAC address for
    :param mac_address: MAC address to set for VM
    :raises: RunTimeError
    """
    nic_label = 'Network adapter 1'
    virtual_nic_device = None
    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
                and dev.deviceInfo.label == nic_label:
            virtual_nic_device = dev
    if not virtual_nic_device:
        raise RuntimeError('{} could not be found.'.format(nic_label))

    virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_nic_spec.device = virtual_nic_device
    virtual_nic_spec.device.macAddress = mac_address
    virtual_nic_spec.device.addressType = "Manual"

    dev_changes = []
    dev_changes.append(virtual_nic_spec)
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm.ReconfigVM_Task(spec=spec)
    wait_for_tasks(service_instance, [task])

    print('MAC address set successfully')
