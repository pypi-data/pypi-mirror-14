# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='stacks-page',
    packages=find_packages(),
    version='0.3',
    author=u'Jonathan Ellenberger',
    author_email='jonathan_ellenberger@wgbh.org',
    url='http://stacks.wgbhdigital.org/',
    license='MIT License, see LICENSE',
    description="A Stacks application for generating static HTML pages.",
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'django-versatileimagefield>=1.0.2',
        'django-textplusstuff>=0.4',
        'Fabric>=1.10.1'
    ],
    package_data={
        'stacks_page': [
            'static/sass/stacks_page/*.scss',
            'static/js/*.js',
            'templates/stacks_page/*.html'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha'
    ]
)
