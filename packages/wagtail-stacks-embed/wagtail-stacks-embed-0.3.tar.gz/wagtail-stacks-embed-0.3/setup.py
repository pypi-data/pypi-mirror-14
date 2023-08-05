# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='wagtail-stacks-embed',
    packages=find_packages(),
    version='0.3',
    author=u'Jonathan Ellenberger',
    author_email='jonathan_ellenberger@wgbh.org',
    url='http://stacks.wgbhdigital.org/',
    license='MIT License, see LICENSE',
    description=(
        "A Wagtail Stacks application for handling embeddable media."
    ),
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'wagtail-streamfieldtools>=0.1',
        'requests==2.5.1'
    ],
    package_data={
        'wagtail_stacks_embed': [
            'static/images/*.png',
            'static/sass/*.scss',
            'static/js/*.js',
            'pbs_cove/static/js/*.js',
            'pbs_cove/static/sass/*.scss',
            'templates/wagtail_stacks_embed/single/*.html',
            'templates/wagtail_stacks_embed/list/*.html'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha'
    ]
)
