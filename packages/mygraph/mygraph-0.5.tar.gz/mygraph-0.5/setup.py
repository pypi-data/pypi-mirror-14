from distutils.core import setup
from distutils.extension import Extension
import os
print 'This module requires libboost-python-dev, libpython-dev, libpqxx-4.0, libhdf5-dev'
srcs = ['./src/' + i for i in os.listdir('./src')]
headers = ['./header/' + i for i in os.listdir('./header')]
inc = ['/usr/include/python2.7', '/usr/include/boost', '/usr/include', './header']
lib = ['/usr/lib', '/opt/local/lib']

setup(name='mygraph',
      version='0.5',
      description='Python hyperpath algorithm implementation',
      author='Tonny Ma',
      author_email='tonny.achilles@gmail.com',
      url='http://fukudalab.hypernav.mobi',
      data_files=[('header', headers)],
      ext_modules=[
          Extension("mygraph",
                    define_macros=[('MAJOR_VERSION', '0'), ('MINOR_VERSION', '5')],
                    include_dirs=inc,
                    library_dirs=lib,
                    libraries=['boost_python', 'python2.7', 'pqxx', 'hdf5', 'hdf5_hl'],
                    extra_compile_args=['-std=c++0x'],
                    sources=srcs)
      ])
