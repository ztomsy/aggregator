try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Project is aim to store data from exchanges api to remote db',
    'author': 'Nekrasov Pavel',
    'version': '0.1.1',
    'install_requires': [''],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'yat-aggregator'
}

setup(**config)
