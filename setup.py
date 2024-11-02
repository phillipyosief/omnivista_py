from setuptools import setup, find_packages

setup(
    name='omnivista_py',
    version='0.3.6',
    packages=find_packages(),
    install_requires=['requests'],
    description='A Python library that simplifies interaction with the OmniVista API, enabling easy authentication, device management, and performance data querying.',
    author='Phillip Jerome Yosief',
    author_email='phillip.yosief@outlook.com',
    url='https://github.com/phillipyosief/omnivista_py',
)