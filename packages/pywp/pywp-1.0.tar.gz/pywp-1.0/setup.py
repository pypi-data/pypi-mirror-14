
from distutils.core import setup
import setuptools


setup(
    name='pywp',
    version='1.0',
    install_requires=[
        'pymysql',
    ],
    packages=[
        'pywp'
    ],
    entry_points={
        "console_scripts": [
        ]
    },
   )
