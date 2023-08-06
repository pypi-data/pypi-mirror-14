#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python setup.py sdist --formats=gztar,zip bdist --formats=rpm,wininst
# sudo python setup.py register -r https://testpypi.python.org/pypi sdist --formats=gztar bdist --formats=egg upload -r https://testpypi.python.org/pypi
# sudo python setup.py check build_sphinx --source-dir=savReaderWriter/documentation -v
# sudo python setup.py check upload_sphinx --upload-dir=build/sphinx/html

import os
import sys
import platform
import versioneer
try:
    from ez_setup import use_setuptools
    use_setuptools()
except:
    pass  # Tox
from setuptools import setup


# automatic labeling of dists
versioneer.VCS = 'git'
versioneer.versionfile_source = 'savReaderWriter/_version.py'
versioneer.versionfile_build = 'savReaderWriter/_version.py'
versioneer.tag_prefix = 'v'  # tags are like v1.2.0
versioneer.parentdir_prefix = 'savReaderWriter-'


#####
## Set package_data values, depending on install/build
#####

arch = platform.architecture()[0]
is_32bit, is_64bit = arch == "32bit", arch == "64bit"
is_install_mode = 'install' in sys.argv
pf = sys.platform.lower()

## This is included in every platform
package_data = {'savReaderWriter': ['spssio/include/*.*',
                                    'spssio/documents/*',
                                    'spssio/license/*',
                                    'cWriterow/*.*',
                                    'documentation/*.*',
                                    'unit_tests/*.*',
                                    'test_data/*.*',
                                    'README','VERSION', 
                                    'COPYRIGHT']}

## *installing* the package: install only platform-relevant libraries
if is_install_mode:             
    if pf.startswith("win") and is_32bit:
        package_data['savReaderWriter'].append('spssio/win32/*.*')
    elif pf.startswith("win"):
        package_data['savReaderWriter'].append('spssio/win64/*.*')
    elif pf.startswith("lin") and is_32bit:
        package_data['savReaderWriter'].append('spssio/lin32/*.*')
    elif pf.startswith("lin") and is_64bit and os.uname()[-1] == "s390x":
        package_data['savReaderWriter'].append('spssio/zlinux64/*.*')
    elif pf.startswith("lin") and is_64bit:
        package_data['savReaderWriter'].append('spssio/lin64/*.*')
    elif pf.startswith("darwin") or pf.startswith("mac"):
        package_data['savReaderWriter'].append('spssio/macos/*.*')
    elif pf.startswith("aix") and not is_32bit:
        package_data['savReaderWriter'].append('spssio/aix64/*.*')
    elif pf.startswith("hp-ux"):
        package_data['savReaderWriter'].append('spssio/hpux_it/*.*')
    elif pf.startswith("sunos") and not is_32bit:
        package_data['savReaderWriter'].append('spssio/sol64/*.*')
    else:
        msg = "Your platform (%r, %s) is not supported" % (pf, arch)
        raise EnvironmentError(msg)

## *building* the package: include all the libraries
else: 
    package_data['savReaderWriter'].extend(['spssio/win32/*.*',
                                            'spssio/win64/*.*',
                                            'spssio/lin32/*.*',
                                            'spssio/zlinux64/*.*',
                                            'spssio/lin64/*.*',
                                            'spssio/macos/*.*',
                                            'spssio/aix64/*.*'
                                            'spssio/hpux_it/*.*',
                                            'spssio/sol64/*.*'])

email = "@".join(["fomcl", "yahoo.com"])
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()

setup(name='savReaderWriter',
      description='Read and write SPSS files',
      author='Albert-Jan Roskam',
      author_email=email,
      maintainer='Albert-Jan Roskam',
      maintainer_email=email,
      license='MIT',
      long_description=read('README.md'),
      zip_safe=False,
      platforms=['Windows', 'MacOS', 'POSIX'],
      url='https://bitbucket.org/fomcl/savreaderwriter',
      download_url='https://bitbucket.org/fomcl/savreaderwriter/downloads',
      extras_require={'numpy': ["numpy"],
                      'Cython': ["Cython"],},
      packages=['savReaderWriter'],
      package_data=package_data,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Operating System :: POSIX :: AIX',
                   'Operating System :: POSIX :: HP-UX',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: POSIX :: SunOS/Solaris',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3', 
                   'Programming Language :: Python :: 3.4', 
                   'Programming Language :: Python :: 3.5', 
                   'Programming Language :: Cython',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Programming Language :: Python :: Implementation :: PyPy',
                   'Topic :: Database'],
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass()
      )
