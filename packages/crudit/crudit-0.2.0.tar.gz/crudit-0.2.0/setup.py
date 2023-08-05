# Copyright 2016 Diogo Dutra

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from crudit.version import VERSION

from setuptools import setup


long_description = ''
with open('README.md') as readme:
    long_description = readme.read()


setup(
    name='crudit',
    packages=['crudit'],
    version=VERSION,
    description='A CRUD framework',
    long_description=long_description,
    author='Diogo Dutra',
    author_email='dutradda@gmail.com',
    url='https://github.com/dutradda/crudit',
    download_url='http://github.com/dutradda/crudit/archive/master.zip',
    license='Apache 2.0',
    keywords='crud framework sqlalchemy redis elasticsearch',
    setup_requires=[
        'pytest-runner==2.7'
    ],
    tests_require=[
        'mock==1.3.0',
        'pytest==2.9.1'
    ],
    install_requires=[
        'jsonschema==2.5.1',
        'SQLAlchemy==1.0.12'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
