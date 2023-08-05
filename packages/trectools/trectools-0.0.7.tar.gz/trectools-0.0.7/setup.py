from distutils.core import setup
#from Cython.Build import cythonize

from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop


requirements = [
    "pandas>=0.15.0",
    "numpy>=1.0.0",
    "scikit-learn>=0.15",
    "scipy >= 0.10.0",
]

setup(name='trectools',
        version='0.0.7',
        author='Joao Palotti',
        author_email='joaopalotti@gmail.com',
        license='LICENSE.txt',
        install_requires=requirements,
        packages=['trectools'],
        #package_dir = {'': '.'},
        url='http://pypi.python.org/pypi/trectools/',
        description='Python toolkit to read and analyse TREC results.',
        long_description=open('README.txt').read()
)

