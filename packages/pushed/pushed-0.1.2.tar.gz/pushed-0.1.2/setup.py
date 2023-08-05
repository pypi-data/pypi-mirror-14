from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open



setup(
    name="pushed",
    version="0.1.2",
    author="Duncan Gilmore",
    author_email="pypi@digmore.tech",
    url="https://github.com/digmore/pypushedapi/",
    license="MIT",
    description="Unofficial Pushed.co API wrapper",
    long_description=open("README.rst").read(),
    keywords="pushed pushed.co mobile apns ios apple android",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "requests",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=[
        "mock"
    ]
)
