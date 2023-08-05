import os
from distutils.core import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name='case_conversion',
  packages=['case_conversion'],
  version='1.0.0',
  description='convert between different types of cases',
  long_description=read('README.md'),
  license='MIT',
  author='Alejandro Frias',
  author_email='joker454@gmail.com',
  url='https://github.com/AlejandroFrias/case-conversion',
  download_url='https://github.com/AlejandroFrias/case-conversion/tarball/1.0.0',
  keywords=['case', 'convert', 'camel', 'pascal', 'snake'],
  classifiers=[],
)
