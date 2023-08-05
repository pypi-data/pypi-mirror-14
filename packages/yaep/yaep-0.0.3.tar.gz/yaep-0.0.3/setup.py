import os
from distutils.core import setup
from setuptools import find_packages

__version__ = 'Unset'
with open('src/yaep/version.py') as vfp:
    vd = vfp.read().strip()
    __version__ = vd.split('=')[1].strip().strip('\'').strip('"')

requirements = []
if os.path.exists('requirements.txt'):
    requirements = [r.strip() for r in open('requirements.txt')]


config = {
    'description': 'YAEP - Yet Another Environment Package',
    'long_description_markdown_filename': 'README.md',
    'author': 'James Kelly',
    'url': 'https://github.com/jimjkelly/yaep',
    'version': __version__,
    'install_requires': requirements,
    'tests_require': ['nose'],
    'test_suite': 'nose.collector',
    'setup_requires': ['setuptools-markdown'],
    'packages': find_packages('src'),
    'package_dir': {'': 'src'},
    'scripts': [],
    'name': 'yaep',
    'zip_safe': False,
}

setup(**config)
