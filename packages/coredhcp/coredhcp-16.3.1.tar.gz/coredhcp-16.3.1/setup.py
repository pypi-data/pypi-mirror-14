from distutils.core import setup
from setuptools import find_packages
from distutils.command.install import install as _install


setup(
  name = 'coredhcp',
  packages = find_packages(exclude=['config']),
  version = '16.03.01',
  description = 'DHCP support for isolated networks in CoreCluster IaaS',
  author = 'Marta Nabozny',
  author_email = 'marta.nabozny@cloudover.io',
  url = 'http://cloudover.org/coredhcp/',
  download_url = 'https://github.com/cloudOver/CoreDhcp/archive/master.zip',
  keywords = ['corecluster', 'cloudover', 'cloud', 'cloudinit'],
  classifiers = [],
  install_requires = ['corecluster'],
)
