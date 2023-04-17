from setuptools import setup, find_packages

setup(
    name='discotoolkit',
    version='1.0',
    packages=find_packages(include=["discotoolkit", "discotoolkit.*"]),
    install_requires=[
        'numpy',
        'pandas',
    ],
)