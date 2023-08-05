import re
from setuptools import setup, find_packages

with open("README.rst", "rb") as f:
	long_descr = f.read().decode("utf-8")

setup(
	name = "pylot-dojo",
	packages = find_packages(),
	entry_points = {
 			"console_scripts": ["Pylot = src.pylot:main"]
		},
	version = "0.1.0",
	description = "MVC framework build on top of flask",
	long_description = long_descr,
	author = "Ketul Patel, Jimmy Jun, Oscar Vazquez, Pariece Mckinney",
	author_email = "ovazquez@gmail.com",
	url = "https://github.com/Ketul-Patel/Pylot"
)