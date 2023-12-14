#from setuptools import setup
from setuptools import setup, find_packages

setup(
    name='UtilsDB',
    version='0.0.7',
    description='Utility functions for SQL Server connections and queries',
    url='git@github.com:volimcvijece/UtilsDB.git',
    author='Tonko Caric',
    author_email='caric.tonko@gmail.com',
    license='unlicensed',
    packages=find_packages(),
    #packages=['utilsdb'], #packages=find_packages()
    # Needed for dependencies
    #install_requires=['pandas', 'pyodbc', 'numpy'], #no nr - any version. specify - "numpy>=1.13.3"
    install_requires=['pandas', 'pymssql', 'numpy'], #no nr - any version. specify - "numpy>=1.13.3"
    zip_safe=False
)