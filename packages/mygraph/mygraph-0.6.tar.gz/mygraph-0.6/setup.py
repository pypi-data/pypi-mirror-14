from distutils.core import setup
from distutils.extension import Extension
import os
import sys
print 'This module requires libboost-python-dev, libpython-dev, libpqxx-4.0, libhdf6-dev'
srcs = ['./src/' + i for i in os.listdir('./src')]
headers = ['./header/' + i for i in os.listdir('./header')]
inc = ['./header']
if 'C_INCLUDE_PATH' in os.environ.keys():
    c_inc = os.environ.get('C_INCLUDE_PATH').split('')
    c_inc.remove('')
    inc += c_inc

if 'CPLUS_INCLUDE_PATH' in os.environ.keys():
    cplus_inc = os.environ.get('CPLUS_INCLUDE_PATH').split('')
    cplus_inc.remove('')
    inc += cplus_inc

for i in os.environ.get('PATH').split(':'):
    if 'include' in i:
       inc.append(i)

inc = list(set(inc))

lib = ''
if sys.platform == 'darwin':
    lib = os.environ.get('LD_LIBRARY_PATH').split(':')
elif sys.platform.startswith('linux'):
    lib = os.environ.get('DYLD_LIBRARY_PATH').split(':')
lib.remove('')

setup(name='mygraph',
      version='0.6',
      description='Python hyperpath algorithm implementation',
      author='Tonny Ma',
      author_email='tonny.achilles@gmail.com',
      url='http://fukudalab.hypernav.mobi',
      data_files=[('header', headers)],
      ext_modules=[
          Extension("mygraph",
                    define_macros=[('MAJOR_VERSION', '0'), ('MINOR_VERSION', '6')],
                    include_dirs=inc,
                    library_dirs=lib,
                    libraries=['boost_python', 'python2.7', 'pqxx', 'hdf5', 'hdf5_hl'],
                    extra_compile_args=['-std=c++0x'],
                    sources=srcs)
      ])
