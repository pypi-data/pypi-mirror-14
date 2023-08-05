import re
from setuptools import setup, find_packages

with open("README.rst", "rb") as f:
	long_descr = f.read().decode("utf-8")

setup(
	name = "gen_pip",
	packages = find_packages(),
	include_package_data=True,
	entry_points = {
 			"console_scripts": ['gen_pip = src.gens:main']
		},
	version = '0.1.0',
	description = "",
	long_description = long_descr,
	author = "",
	author_email = "",
	url = ""
)