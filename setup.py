from setuptools import setup, find_packages

# Read the contents of the requirements.txt file
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='discotoolkit',
    version="1.1.4",
    url='http://www.immunesinglecell.org/',
    author='Li Mengwei, Rom Uddamvathanak',
    author_email='uddamvathanak_rom@immunol.a-star.edu.sg',
    description='DISCOtoolkit is an python package that allows users to access data and use the tools provided by the DISCO database.',
    packages=find_packages(include=["discotoolkit", "discotoolkit.*"]),
    install_requires=requirements,
    python_requires = '>=3.8.16',
    include_package_data=True,
    long_description="DISCOtoolkit is an python package that allows users to access data and use the tools provided by the DISCO database. \
        It provides the following functions\nFilter and download DISCO data based on sample metadata and cell type information\nCELLiD: \
            cell type annotation\nscEnrichment: geneset enrichment using DISCO DEGs",
)