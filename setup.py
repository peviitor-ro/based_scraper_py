from setuptools import setup, find_packages

setup(
    name='peviitor_scraper',
    version='0.0.1',
    description='A simple scraper',
    url="",
    author='Peviitor',
    
    packages=find_packages(),

    install_requires=[
        'beautifulsoup4==4.9.3',
        'bs4==0.0.1',
        'certifi==2020.12.5',
        'chardet==4.0.0',
        'idna==2.10',
        'lxml==4.9.2',
        'requests==2.25.1',
        'soupsieve==2.2',
        'urllib3==1.26.3',
        'selenium==3.141.0',
    ],
    python_requires='>=3.6',
)