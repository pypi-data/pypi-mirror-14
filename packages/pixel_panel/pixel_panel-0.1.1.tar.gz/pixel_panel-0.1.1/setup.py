#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Pillow>=3.1.1',
    'pytest>=2.9.1',
    'sphinx-rtd-theme>=0.1.9',
    'coverage>=4.0.3',
    'pytest-cov>=2.2.1',
]

setup(
    name='pixel_panel',
    version='0.1.1',
    description="Library for generating a customizable information panel that's suitable for rendering on an LED matrix display.",
    long_description=readme + '\n\n' + history,
    author="Greg Harfst",
    author_email='gharfst@gmail.com',
    url='https://github.com/nodogbite/pixel_panel',
    packages=[
        'pixel_panel',
    ],
    package_dir={'pixel_panel':
                 'pixel_panel'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pixel_panel',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
)
