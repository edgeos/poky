ESXi VM management
==================

manage-esxi-vm tool for managing VMs on ESXi servers. Supports deploy (using
ovftool), set MAC address, start, stop, and destroy for VMs. Based off samples
from https://github.com/vmware/pyvmomi-community-samples, which use
https://github.com/vmware/pyvmomi. Supports both python and python3.

## Installation

Install using setuptools:

sudo python setup.py install

VM deployment requires ovftool (https://www.vmware.com/support/developer/ovf/).
