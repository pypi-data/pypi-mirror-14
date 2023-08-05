#!/usr/bin/env python

from setuptools import setup

setup(
	name='LocationWebApp', 
	version='3.1.2',                     
	packages=['LocationWebApp'],
	author='Savithru Lokanath',
	author_email='savithru@icloud.com',
	classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='MIT',
	url='http://savithruml.github.io/LocationWebApp/',
	download_url='https://github.com/savithruml/LocationWebApp/tarball/master',
	description='A web-application to show your current location on a Google Map & to obtain location data such as latitude, longitude & zip-code',
	install_requires=['flask-googlemaps','tornado','requests'],
)

