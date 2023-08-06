from setuptools import setup

setup(
    name='libvmware',
    version='0.1',
    description='Simple library for working with VMWare',
    author='Austin Simmons',
    author_email='austin@simmons-tech.net',
    packages=['libvmware'],
    install_requires= [
        'pyvmomi',
        'requests'
    ],
    zip_safe=False
)
