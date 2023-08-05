import os

from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    description = f.read()

setup(
    name = 'sphinx-navtree',
    version = '0.2.1',
    description = 'Navigation tree customization for Sphinx',
    long_description = '\n' + description,
    url = 'https://github.com/bintoro/sphinx-navtree',
    author = 'Kalle Tuure',
    author_email = 'kalle@goodtimes.fi',
    license = 'MIT',
    packages = ['sphinx_navtree'],
    package_data = {
        'sphinx_navtree': ['*.css'],
    },
    install_requires = [],
    classifiers = [
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ]
)
