import os
from setuptools import setup, setuptools

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='tag-processor',
    version='0.1.6',
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='BSD',
    description='Application for processing tags inside string, like ${tag}',
    url='https://bitbucket.org/creekmind/tag_processor/',
    author='Petr Kapsamun',
    author_email='creekmind@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)