# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname

from beauty_view import __version__

setup(
    name='django-beauty-view',
    version=__version__,
    author='Dmitry Voronkov',
    author_email='mail@voronkovd.ru',
    url='https://bitbucket.org/voronkovd/django-beauty-view',
    description='Beauty Django Views Mixin',
    long_description=open('README.txt').read(),
    license='GNU General Public License',
    install_requires=('Django>=1.4',),
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
