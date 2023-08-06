from setuptools import setup, find_packages
from codecs import open
from os import path
import file_readers.metadata as metadata

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# TODO: Currently not working because of markdown to reStructuredText conversion not added.
long_description = ""
if path.exists(path.join(here, 'README.rst')):
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name=metadata.NAME,
    version=metadata.VERSION,
    description=metadata.DESCRIPTION,
    long_description=long_description,
    url=metadata.URL,
    author=metadata.AUTHOR,
    author_email=metadata.AUTHOR_EMAIL,
    license=metadata.LICENSE,
     # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['csv/tests', 'excel/tests']),
    setup_requires=['nose>=1.0', 'coverage>=4.0.3', 'openpyxl>=2.3.4'],
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=['openpyxl'],
)
