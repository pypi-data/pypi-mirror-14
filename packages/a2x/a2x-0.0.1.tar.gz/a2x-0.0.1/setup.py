from setuptools import setup, find_packages
import a2x

setup(
    name='a2x',
    version=a2x.__version__,
    author=a2x.__author__,
    author_email=a2x.__email__,
    description=a2x.__description__,
    long_description=a2x.__long_description__,
    url='https://k0st1an.github.io/',
    packages=find_packages(),
    install_requires=[],
    scripts=['a2x-test.py']
)
