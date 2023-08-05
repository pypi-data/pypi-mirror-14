from setuptools import setup, find_packages

setup(
    # Application name:
    name="PiVideo",

    # Version number (initial):
    version="0.0.5",

    # Application author details:
    author="Lintest Systems LLC",
    author_email="lintestsystems@gmail.com",

    # Packages
    packages= find_packages(),

    # Include additional files into the package
    #include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/pivideo_v005/",

    # License
    license="MIT",

    # keywords
    keywords="PiCapture Raspberry Pi Video",

    description="Raspberry Pi PiVideo Utilities for PiCapture",
    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    # install_requires=[
    #    "smbus-cffi",
    # ],
     
    py_modules=['pivideo','pivideo_cmd'], 
     
    entry_points={
       'console_scripts': [
           'pivideo = pivideo_cmd:main',
           'pivideo_cmd = pivideo_cmd:main',
       ],
    }
)