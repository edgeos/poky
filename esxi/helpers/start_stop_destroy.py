"""
Functions to start/stop/destroy VM using vSphere API (pyVmomi). Based off
samples from https://github.com/vmware/pyvmomi-community-samples

start/stop based off:
https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/virtual_machine_power_cycle_and_question.py

destroy based off:
https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/destroy_vm.py

"""
from pyVmomi import vim
from .tasks import wait_for_tasks


def start_vm(service_instance, vm):
    """Starts VM using given VM object and service instance, waits till start
    operation finishes, raises exception on failure
    :param service_instance: Service Instance for ESXi server
    :param vm: VM object corresponding to VM to set MAC address for
    :raises: task.info.error?
    """
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM already powered on")
    else:
        task = vm.PowerOn()
        wait_for_tasks(service_instance, [task])
        print("VM successfully powered on")


def stop_vm(service_instance, vm):
    """Stops VM using given VM object and service instance, waits till stop
    operation finishes, raises exception on failure
    :param service_instance: Service Instance for ESXi server
    :param vm: VM object corresponding to VM to set MAC address for
    :raises: task.info.error?
    """
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        print("VM already powered off")
    else:
        task = vm.PowerOff()
        wait_for_tasks(service_instance, [task])
        print("VM successfully powered off")


def destroy_vm(service_instance, vm):
    """Destroys VM using given VM object and service instance, wait till
    destroy operation finishes, raises exception on failure
    :param service_instance: Service Instance for ESXi server
    :param vm: VM object corresponding to VM to set MAC address for
    :raises: task.info.error?
    """
    # Stop the VM first
    stop_vm(service_instance, vm)
    task = vm.Destroy_Task()
    wait_for_tasks(service_instance, [task])
    print("VM successfully destroyed")
