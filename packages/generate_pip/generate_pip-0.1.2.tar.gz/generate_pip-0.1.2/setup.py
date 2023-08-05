import re
from setuptools import setup, find_packages


with open("README.rst", "rb") as f:
   long_descr = f.read().decode("utf-8")

setup(
   name = "generate_pip",
   packages = find_packages(),
   include_package_data = True,
   entry_points = {
       "console_scripts": ['generate_pip = src.generate_pip:main']
       },
   version = '0.1.2',
   description = "PIP skeleton generator",
   long_description = long_descr,
   author = "Oscar Vazquez",
   author_email = "oscar.vazquez2012@gmail.com",
   url = "https://github.com/oscarvazquez/generate_pip"
)