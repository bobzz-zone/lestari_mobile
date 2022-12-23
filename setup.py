from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in lestari_mobile/__init__.py
from lestari_mobile import __version__ as version

setup(
	name="lestari_mobile",
	version=version,
	description="For Mobile API",
	author="DAS",
	author_email="digitalasiasolusindo@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
