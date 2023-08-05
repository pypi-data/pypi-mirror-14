import os
import codecs
from setuptools import setup


__version__ = '0.1'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requirements = [
    'requests >= 2.9.1',
]

test_requirements = [
    'py==1.4.31',
    'pyflakes==1.1.0',
    'pytest==2.9.0',
    'pytest-cache==1.0',
    'pytest-flakes==1.0.1',
    'pytest-pep8==1.0.6',
    'factory-boy==2.6.1',
    'mock==1.0.1',
    'pep8==1.7.0',
]

docs_requirements = [
    'Sphinx==1.3.7',
    'sphinx_rtd_theme==0.1.9'
]

setup(
    name='python-nasapi',
    version=__version__,
    description='Python-nasapi is a client library for the NASA api endpoints.',
    long_description=read('README.rst'),
    author='Carlo Smouter',
    author_email='lockwooddev@gmail.com',
    url='https://github.com/lockwooddev/python-nasapi',
    install_requires=install_requirements,
    extras_require={
        'tests': test_requirements,
        'docs': docs_requirements,
    },
    license='MIT',
    keywords=['nasa', 'api'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[
        'nasapi',
        'nasapi.tests',
        'docs',
    ],
)
