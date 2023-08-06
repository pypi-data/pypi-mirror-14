from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from setuptools import setup, find_packages


version = '1.0.2'

setup(
    name='ripozo-sqlalchemy',
    version=version,
    packages=find_packages(include=['ripozo_sqlalchemy', 'ripozo_sqlalchemy.*']),
    url='https://github.com/vertical-knowledge/ripozo-sqlalchemy',
    license='',
    author='Tim Martin',
    author_email='tim.martin@vertical-knowledge.com',
    description=('Integrates SQLAlchemy with ripozo to'
                 ' easily create sqlalchemy backed Hypermedia/HATEOAS/REST apis'),
    install_requires=[
        'ripozo',
        'SQLAlchemy>=0.9.1'
    ],
    tests_require=[
        'unittest2',
        'tox',
        'mock',
        'pylint'
    ],
    test_suite="ripozo_sqlalchemy_tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)