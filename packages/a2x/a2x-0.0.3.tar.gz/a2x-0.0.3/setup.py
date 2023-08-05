from setuptools import setup, find_packages
import a2x

setup(
    name='a2x',
    version=a2x.__version__,
    author=a2x.__author__,
    author_email=a2x.__email__,
    description=a2x.__description__,
    # long_description=a2x.__long_description__,
    keywords=['valve', 'a2s',],
    url='https://github.com/k0st1an/a2x',
    packages=find_packages(),
    install_requires=[],
    license='Apache License Version 2.0',
    scripts=['a2x-test.py'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
