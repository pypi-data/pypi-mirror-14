#!/usr/bin/env python

from distutils.core import setup
setup(
  name = 'bootdev',
  #packages = ['bootdev'], # this must be the same as the name above
  version = '0.2',
  description = 'Bootdev command for AWS deployments',
  author = 'chankongching',
  author_email = 'chankongching@gmail.com',
  url = 'https://github.com/chankongching/bootdev', # use the URL to the github repo
  download_url = 'https://github.com/chankongching/bootdev/tarball/0.1', 
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  license='MIT',
  scripts=['bin/bootdev'],
  include_package_data = True,
  data_files = [('', ['templates/*.template'])],
  package_data={'bootdev':['templates/*.template']},
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
