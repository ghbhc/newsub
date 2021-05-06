from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name = 'newsub',
	version = '0.3.2',
	author = 'ghbhc',
	author_email = 'ghbhc01@gmail.com',
	description = 'expdite the creation of Slurm submission scripts',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	packages = find_packages(),
	url = 'https://github.com/ghbhc/newsub',
	entry_points = {
		'console_scripts': [
		'newsub = newsub.main:main'
		]
	},
	python_requires = '>=3.6'
)
