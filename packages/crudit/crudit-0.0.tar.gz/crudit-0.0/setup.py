from distutils.core import setup
setup(
    name = 'crudit',
    packages = [],
    version = '0.0',
    description = 'A CRUD framework with Abstract, SQLAlchemy, Redis and ElasticSearch (separated and together) '
        'implementations. Operations implemented are: insert, update, delete, get, get all and get many.',
    author = 'Diogo Dutra',
    author_email = 'dutradda@gmail.com',
    url = 'https://github.com/dutradda', # use the URL to the github repo
    # download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
    keywords = ['crud', 'framework', 'sqlalchemy', 'redis', 'elasticsearch'], # arbitrary keywords
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
