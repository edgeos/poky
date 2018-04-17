"""
Helper functions for use by other modules for using vSphere API
"""
import atexit
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

ESXI_VSPHERE_PORT = 443


def get_service_instance(host, username, password, port=ESXI_VSPHERE_PORT):
    """Get a service connection to ESXi host using given credentials
    :param host: ESXi server IP address or name
    :param username: username for account on host
    :param password: password for account on host
    :param port: port number of vSphere service
    :return: Service instance object for use in configuring VMs
    :raises: RunTimeError
    """
    # Connect to ESXi vSphere service
    # Ignore certificate verification failures for test ESXi server
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    service_instance = SmartConnect(host=host,
                                    user=username,
                                    pwd=password,
                                    port=port,
                                    sslContext=ctx)

    if not service_instance:
        raise RuntimeError("Could not connect to %s:%s as %s with "
                           "given password" % (args.host, port, args.user))

    atexit.register(Disconnect, service_instance)

    return service_instance


def get_vm(service_instance, vm_name):
    """Get VM object with given vm_name, using given service_instance for
    ESXi server.
    :param service_instance: Service Instance for ESXi server
    :param vm_name: Name of VM on ESXi server
    :return: VM object
    :raises: RunTimeError
    """
    print('Searching for VM {}'.format(vm_name))
    content = service_instance.RetrieveContent()
    containerView = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True)
    for container in containerView.view:
        if container.name == vm_name:
            return container

    raise RuntimeError('VM "%s" not found' % vm_name)
