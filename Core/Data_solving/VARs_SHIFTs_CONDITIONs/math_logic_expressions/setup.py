
	  
from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='token_posfix_calculation',
  version='0.0',
  author='wolkolak1',
  author_email='wolkolak1@gmail.com',
  description='Tokeniztion, posfixing and postfix calculation',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/wolkolak',
  packages=['token_posfix_calculation'],
  install_requires=['requests>=2.25.1'],
  classifiers=[
	'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.8.8',
    'License :: OSI Approved :: MIT License',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
    'Operating System :: OS Independent'
  ],
  keywords='python algorithm postfix calculation',
  project_urls={
    'Documentation': 'link'
  },
)