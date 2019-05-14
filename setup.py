try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Project is aim to store data from exchanges api to remote db',
    'author': 'Nekrasov Pavel',
    'version': '0.0.4.2',
    'install_requires': [''],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'tkg-interfaces'
}

setup(**config)
