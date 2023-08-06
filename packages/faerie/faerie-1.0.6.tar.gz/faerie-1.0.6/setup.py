from distutils.core import setup
from setuptools import Extension,find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
  name = 'faerie',
  version = '1.0.6',
  description = 'Dictionary-based entity extraction with efficient filtering',
  author = 'Zheng Tang',
  author_email = 'zhengtan@isi.edu',
  url = 'https://github.com/ZhengTang1120/entity_extraction/', # use the URL to the github repo
  packages = find_packages(),
  keywords = ['heap', 'entity_extraction'], # arbitrary keywords
  ext_modules=[Extension(
        'singleheap',
        ['singleheap.c'])],
  entry_points ={
        'console_scripts': [
            'faerie = faerie.faerie.faerie:consolerun'
        ]
    },
  install_requires=['nltk']
)


# from distutils.core import setup, Extension
# singleheap_methods = Extension('singleheap', sources = ['singleheap.c'])
# setup(name = "singleheap1",
#     version = "1.0",
#     description = "singleheap",
#     ext_modules = [singleheap_methods], 
# )