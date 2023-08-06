#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests==2.9.1",
    "schedule==0.3.2",
    "click==6.3",
    "html5lib==0.9999999",
    "beautifulsoup4==4.4.1",
    "tomorrow==0.2.4"
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='course_backup',
    version='0.1.2',
    description="backup open edx courses",
    long_description=readme + '\n\n' + history,
    author="wenjie wu",
    author_email='wuwenjie718@gmail.com',
    url='https://github.com/wwj718/course_backup',
    packages=[
        'course_backup',
    ],
    package_dir={'course_backup':
                 'course_backup'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='course_backup',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
         'console_scripts': [
                         'course_backup = course_backup.course_backup:main'
            ]
        }
)
