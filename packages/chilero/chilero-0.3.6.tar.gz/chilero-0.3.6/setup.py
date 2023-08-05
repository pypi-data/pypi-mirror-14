from distutils.core import setup

from setuptools import find_packages

setup(
    name='chilero',
    use_scm_version=True,
    namespace_packages=['chilero'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/dmonroy/chilero',
    author='Darwin Monroy',
    author_email='contact@darwinmonroy.com',
    description='A micro framework... A la Tortrix!',
    install_requires=[
        'aiohttp>=0.21',
    ],
    setup_requires=[
        'setuptools_scm',
    ]
)
