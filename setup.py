from setuptools import setup

setup(
    name='UtilsDB',
    version='0.0.2',
    description='Utility functions for SQL Server connections and queries',
    url='git@github.com:volimcvijece/UtilsDB.git',
    author='Tonko Caric',
    author_email='caric.tonko@gmail.com',
    license='unlicensed',
    packages=['utilsdb'],
    # Needed for dependencies
    install_requires=['pandas', 'pyodbc', 'numpy'], #no nr - any version. specify - "numpy>=1.13.3"
    zip_safe=False
)