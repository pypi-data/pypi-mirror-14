import re
from setuptools import setup

version = re.search(
   '^__version__\s*=\s*"(.*)"',
   open('awesome_pip_module/awesome_module.py').read(),
   re.M
   ).group(1)

with open("README.rst", "rb") as f:
   long_descr = f.read().decode("utf-8")

   setup(
   name = "awesome_module",
   packages = ["awesome_pip_module"],
   entry_points = {
       "console_scripts": ['awesome_module = awesome_pip_module.awesome_module:awesome_module']
       },
   version = version,
   description = "Python command line html creator",
   long_description = long_descr,
   author = "Brian Saminathen",
   author_email = "briansaminathen@hotmail.com",
   url = "https://github.com/techin99/awesome_pip_module.git"
) 

