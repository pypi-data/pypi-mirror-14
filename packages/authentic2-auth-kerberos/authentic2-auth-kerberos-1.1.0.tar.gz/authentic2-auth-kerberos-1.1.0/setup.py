#! /usr/bin/env python

import subprocess
import os

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist


class version_sdist(sdist):
    def run(self):
        print "creating VERSION file"
        if os.path.exists('VERSION'):
            os.remove('VERSION')
        version = get_version()
        version_file = open('VERSION', 'w')
        version_file.write(version)
        version_file.close()
        sdist.run(self)
        print "removing VERSION file"
        if os.path.exists('VERSION'):
            os.remove('VERSION')


def get_version():
    '''Use the VERSION, if absent generates a version with git describe, if not
       tag exists, take 0.0.0- and add the length of the commit log.
    '''
    if os.path.exists('VERSION'):
        with open('VERSION', 'r') as v:
            return v.read()
    if os.path.exists('.git'):
        p = subprocess.Popen(['git', 'describe', '--dirty', '--match=v*'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result = p.communicate()[0]
        if p.returncode == 0:
            result = result.split()[0][1:]
        else:
            result = '0.0.0-%s' % len(subprocess.check_output(
                ['git', 'rev-list', 'HEAD']).splitlines())
        return result.replace('-', '.').replace('.g', '+g')
    return '0.0.0'


setup(
    name='authentic2-auth-kerberos',
    version=get_version(),
    license='AGPLv3',
    description='Authentic2 Auth Kerberos',
    long_description=open('README').read(),
    author="Entr'ouvert",
    author_email="info@entrouvert.com",
    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    package_data={
        'authentic2_auth_kerberos': [
            'templates/authentic2_auth_kerberos/*.html',
            'templates/django_kerberos/*.html',
            'static/authentic2_auth_kerberos/js/*.js',
            'static/authentic2_auth_kerberos/css/*.css',
            'static/authentic2_auth_kerberos/img/*.png',
        ],
    },
    install_requires=[
        'authentic2',
        'django-kerberos',
    ],
    entry_points={
        'authentic2.plugin': [
            'authentic2-auth-kerberos = authentic2_auth_kerberos:Plugin',
        ],
    },
    cmdclass={'sdist': version_sdist})
