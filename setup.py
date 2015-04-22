# -*- coding: utf-8 -*-
"""
Flask-SockJS
-------------

Simple integration of Flask and SockJS
"""
from setuptools import setup

setup(
    name='Flask-SockJS',
    version='0.1.0',
    url='http://github.com/cravler/flask-sockjs/',
    license='MIT',
    author='Sergei Vizel',
    author_email='sergei.vizel@gmail.com',
    description='Simple integration of Flask and SockJS',
    long_description=__doc__,
    py_modules=['flask_sockjs'],
    packages=['flask_sockjs'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'Twisted', 'Flask-Twisted', 'txsockjs', 'observable'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)