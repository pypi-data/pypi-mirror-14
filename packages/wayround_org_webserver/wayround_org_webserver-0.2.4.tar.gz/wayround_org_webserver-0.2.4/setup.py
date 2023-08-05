#!/usr/bin/python3

from setuptools import setup

setup(
    name='wayround_org_webserver',
    version='0.2.4',
    description='homebrewn webserver',
    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='https://github.com/AnimusPEXUS/wayround_org_webserver',
    install_requires=[
        'wayround_org_utils',
        'wayround_org_socketserver'
        ],
    packages=[
        'wayround_org.webserver',
        'wayround_org.webserver.modules',
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
        ],
    entry_points={
        'console_scripts': [
            'wrows = wayround_org.webserver.main'
            ],
        }
    )
