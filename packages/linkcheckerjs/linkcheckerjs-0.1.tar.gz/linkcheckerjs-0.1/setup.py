import os
import json
from setuptools import setup, find_packages
from distutils.command.build_py import build_py as _build_py
from distutils.command.build_ext import build_ext as _build_ext

import subprocess

# Hack to prevent TypeError: 'NoneType' object is not callable error
# on exit of python setup.py test
try:
    import multiprocessing
except ImportError:
    pass


version = '0.1'


class CreateSymlink(_build_ext):

    def run(self):
        print 'Create symlinks'
        if not os.path.exists('linkcheckerjs/node_modules'):
            os.symlink('../node_modules', 'linkcheckerjs/node_modules')
        if not os.path.exists('linkcheckerjs/jslib'):
            os.symlink('../jslib', 'linkcheckerjs/jslib')
        _build_ext.run(self)


class NpmInstall(_build_py):

    def run(self):
        print 'Installing node packages'
        p = subprocess.Popen(["npm install"], shell=True)
        p.communicate()

        path = os.path.join(self.build_lib, 'linkcheckerjs')
        print 'Create folder', path
        if not os.path.exists(path):
            os.makedirs(path)

        print 'Create symlinks'
        if not os.path.exists('build/lib/linkcheckerjs/node_modules'):
            os.symlink('../../../node_modules', 'build/lib/linkcheckerjs/node_modules')
        if not os.path.exists('build/lib/linkcheckerjs/jslib'):
            os.symlink('../../../jslib', 'build/lib/linkcheckerjs/jslib')
        _build_py.run(self)


setup(
    cmdclass={'build_py': NpmInstall, 'build_ext': CreateSymlink},
    name='linkcheckerjs',
    version=version,
    description="Check links and resources in web page or full website",
    long_description=open('README.rst').read().split('Build Status')[0],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

    ],
    keywords='checker,link,website,validation,crawler',
    author='Aur\xc3\xa9lien Matouillot',
    author_email='a.matouillot@gmail.com',
    url='Check links and resources in web page or full website',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'requests',
        'colorterm',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    linkcheckerjs = linkcheckerjs.run:main
    linkreaderjs = linkcheckerjs.reader:main
    """,
)
