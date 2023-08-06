#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from distutils.core import setup

setup(
    name='wstund',
    version='0.1.5',
    author='yumaokao',
    author_email='ymkq9h@gmail.com',
    description='A WebSocket Tunnel Daemon.',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    url='http://www.github.com',

    packages=['wstund'],
    install_requires=[
        'ws4py',
        'python-pytun',
        'lockfile',
        'python-daemon',
        'cherrypy'
    ],
    entry_points={
        'console_scripts': ['wstund=wstund.wstund:sudo_main']
    }
)
