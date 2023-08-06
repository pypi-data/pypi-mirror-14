from distutils.core import setup

from setuptools import setup


setup(name='pypiTest',
  version='0.1.0',
  description='First pip pack',
  author='facode',
  author_email='floare.alin.fa@gmail.com',
  license='Apache2',
  packages=['facode-piptest'],
  install_requires=[
    'ipython',
    'scrapy'
  ],

  url='https://codeload.github.com/FACode/pip-test/',
  download_url='https://codeload.github.com/FACode/pip-test/tarball/0.1'

)

#  url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
#  download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
