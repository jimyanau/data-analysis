from setuptools import setup, find_packages

setup(
		name='data-analysis',
		version='0.0.1',
		url='https://github.com/jimyanau/data-analysis',
		license='BSD',
		author='Jim Yan',
		package=find_packages(),
		install_requires=['PyQt5', 
						 'pandas', 
						 'sqlalchemy',
						 'nltk',
						 'numpy', 
						 'jupyter', 
						 'python-twitter'],
		entry_points={},
		exras_require={'dev':['flake8']},
		)