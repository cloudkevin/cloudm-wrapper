from setuptools import setup

with open('README.md', 'r') as fh:
	long_description = fh.read()

setup(name='cloudm-wrapper-cloudkevin',
	version='1.0',
	description='CloudM API Wrapper',
	long_description=long_description,
	long_description_content_type='text/markdown',
	python_requires='>=3.7',
	packages=['cloudm'],
	install_requires=['requests'],
	zip_safe=False)