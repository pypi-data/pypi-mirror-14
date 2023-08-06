#from distutils.core import setup
from setuptools import find_packages,setup

__VERSION__ = '0.9'

setup(
  name = 'gubser',
  packages = ['gubser'], # this must be the same as the name above
  version = __VERSION__,
  setup_requires=["cffi>=1.0.0",
                  "numpy" ],
  install_requires=["cffi>=1.0.0",
                  "numpy" ],
  #packages=find_packages(exclude=["cffi_build"]),
  cffi_modules=["gubser/gubser_cffi.py:ffi",
                "gubser/riemann_cffi.py:ffi"],
  description = 'Gubser solution for ideal hydrodynamics, 2+1D viscous hydrodynamics ',
  author = 'Long-Gang Pang',
  author_email = 'lgpang@qq.com',
  license = 'MIT',
  url = 'https://github.com/snowhitiger/gubser',
  download_url = 'https://github.com/snowhitiger/gubser/tarball/%s'%__VERSION__,
  keywords = ['gubser', '2nd order viscous hydrodynamics', 'python', 'clvisc'],
  classifiers = [],
)
