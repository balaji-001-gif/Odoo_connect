from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __init__.py
__version__ = "0.0.1"

setup(
	name="odoo_connect",
	version=__version__,
	description="Integration between Odoo and Frappe LMS",
	author="Antigravity",
	author_email="bot@antigravity.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
