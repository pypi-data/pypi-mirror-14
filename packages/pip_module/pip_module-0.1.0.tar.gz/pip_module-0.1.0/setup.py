import re
from setuptools import setup


version = re.search(
   '^__version__\s*=\s*"(.*)"',
   open('pip_module/awesome_module.py').read(),
   re.M
   ).group(1)


with open("README.rst", "rb") as f:
   long_descr = f.read().decode("utf-8")


setup(
   name = "pip_module",
   packages = ["pip_module"],
   entry_points = {
       "console_scripts": ['pip_module = pip_module.awesome_module:awesome_module']
       },
   version = version,
   description = "Python module",
   long_description = long_descr,
   author = "Barclay Iversen AKA Spracto",
   author_email = "barclayiversen@gmail.com",
   url = "https://github.com/Spracto/awesome_pip_module"
)
