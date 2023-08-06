#!/usr/bin/env python
from distutils.core import Command
from distutils.command.install import install as _install
import os
# Including all datafiles
datadir = os.path.join('templates')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

from distutils.core import setup
setup(
  name = 'bootdev',
  #packages = ['bootdev'], # this must be the same as the name above
  version = '0.2.6',
  description = 'Bootdev command for AWS deployments',
  author = 'chankongching',
  author_email = 'chankongching@gmail.com',
  url = 'https://github.com/chankongching/bootdev', # use the URL to the github repo
  download_url = 'https://github.com/chankongching/bootdev/tarball/0.1', 
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  license='MIT',
  scripts=['bin/bootdev'],
  include_package_data = True,
  data_files = datafiles,
  #data_files = [('', ['templates/*.template'])],
  package_data={'bootdev':['package.ini']},
  install_requires=[
    'boto3',
    'awscli'
  ],
  classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    #'Programming Language :: Python :: 2',
    #'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    #'Programming Language :: Python :: 3',
    #'Programming Language :: Python :: 3.2',
    #'Programming Language :: Python :: 3.3',
    #'Programming Language :: Python :: 3.4',
  ],
)

from os.path import *
import re
class package_ini(Command):
    """
        Locate package.ini in all installed packages and patch it as requested
        by wildcard references to install process.
    """

    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

    def visit(self, dirname, names):
        packages = self.distribution.get_command_obj(build_py.__name__).packages
        if basename(dirname) in packages:
            if 'package.ini' in names:
                self.patch(join(dirname, 'package.ini'))

    def patch(self, ini_file):
        print 'patching file' + ini_file
        with open(ini_file,'r') as infile:
            file_data = infile.readlines()
        with open(ini_file,'w') as outfile:
            for line in file_data:
                _line = self.patch_line(line)
                if _line:
                    line = _line
                outfile.write(line)

    def patch_line(self, line):
        """
            Patch an installed package.ini with setup's variables
        """
        match = re.match('(?P<identifier>\w+)\s*=.*##SETUP_PATCH\\((?P<command>.*)\.(?P<variable>.*)\\)', line)
        if not match:
            return line
        print 'Replacing:'+line
        line = match.group('identifier')
        line += ' = '
        data = '(self).distribution.get_command_obj(\''+\
                match.group('command')+'\')'+'.'+\
                match.group('variable')
        line += '\''+eval(data)+'\''
        line += '\n'
        print 'With:' + line
        return line

class install(_install):
    from distutils.command.install import install as _install
    sub_commands = _install.sub_commands + [
        (package_ini.__name__, None)
    ]
