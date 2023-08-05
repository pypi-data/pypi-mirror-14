
import re
from setuptools import setup


version = re.search(
   '^__version__\s*=\s*"(.*)"',
   open('new_demo/new_demo.py').read(),re.M).group(1)


with open("README.rst", "rb") as f:
   long_descr = f.read().decode("utf-8")


setup(
   name = "new_demo",
   packages = ["new_demo"],
   entry_points = {
       "console_scripts": ['new_demo = new_demo.new_demo:awesome_module']
       },
   version = version,
   description = "Python command line html creator",
   long_description = long_descr,
   author = "Justin Niu",
   author_email = "jusman@gmail.com",
   url = "https://github.com/oscarvazquez/command_line_tool_demo"
)