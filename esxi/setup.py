from setuptools import find_packages, setup

setup(name='manage-esxi-vm',
      version='1.0',
      description='Tool to manage VM on ESXi server',
      install_requires='pyvmomi>=v6.5.0.2017.5-1',
      packages=find_packages(),
      scripts=['manage-esxi-vm'])
