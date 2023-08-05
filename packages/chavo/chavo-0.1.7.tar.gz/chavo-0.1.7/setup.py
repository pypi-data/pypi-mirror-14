import re
from setuptools import setup, find_packages


version = re.search(
   '^__version__\s*=\s*"(.*)"',
   open('app/chavo.py').read(),
   re.M
   ).group(1)


with open("README.rst", "rb") as f:
   long_descr = f.read().decode("utf-8")

setup(
   name = "chavo",
   packages = find_packages(),
   entry_points = {
       "console_scripts": ['chavo = app.chavo:main']
       },
   version = version,
   description = "Command line html creator",
   long_description = long_descr,
   author = "Oscar Vazquez",
   author_email = "oscar.vazquez2012@gmail.com",
   url = "https://github.com/oscarvazquez/chavo"
)