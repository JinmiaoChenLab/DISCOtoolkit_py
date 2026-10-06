from setuptools import setup, find_packages

# Read the contents of the requirements.txt file
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='discotoolkit',
    version="1.2.0",
    url='https://disco.bii.a-star.edu.sg/',
    author='Li Mengwei, Rom Uddamvathanak',
    author_email='uddamvathanak_rom@immunol.a-star.edu.sg',
    description='DISCOtoolkit is an python package that allows users to access data and use the tools provided by the DISCO database.',
    packages=find_packages(include=["discotoolkit", "discotoolkit.*"]),
    install_requires=requirements,
    python_requires = '>=3.9',
    include_package_data=True,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # shown on the PyPI page
    project_urls={
        "Documentation": "https://disco.bii.a-star.edu.sg/v1/docs/toolkit/guide/",
        "Source": "https://github.com/JinmiaoChenLab/DISCOtoolkit_py",
        "Issues": "https://github.com/JinmiaoChenLab/DISCOtoolkit_py/issues",
        "DISCO": "https://disco.bii.a-star.edu.sg/v1/",
    },
)