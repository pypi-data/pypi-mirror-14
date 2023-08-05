#from distutils.core import setup
from setuptools import find_packages,setup

setup(
  name = 'gubser',
  packages = ['gubser'], # this must be the same as the name above
  version = '0.6',
  setup_requires=["cffi>=1.0.0"],
  install_requires=["cffi>=1.0.0"],
  #packages=find_packages(exclude=["cffi_build"]),
  cffi_modules=["gubser/gubser_cffi.py:ffi"],
  description = 'Gubser solution for ideal hydrodynamics, 2+1D viscous hydrodynamics ',
  author = 'Long-Gang Pang',
  author_email = 'lgpang@qq.com',
  url = 'https://github.com/snowhitiger/gubser',
  download_url = 'https://github.com/snowhitiger/gubser/tarball/0.6',
  keywords = ['gubser', '2nd order viscous hydrodynamics', 'python', 'clvisc'],
  classifiers = [],
)
