import os
from setuptools import setup


README = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')).read()


setup(name='kiseru',
      version='0.0.0',
      description='Make any your functions pipable.',
      long_description=README,
      classifiers=['Programming Language :: Python'],
      keywords='pipe',
      author='mtwtkman',
      author_email='punipuniomochi@gmail.com',
      url='https://github.com/mtwtkman/kiseru',
      license='WTFPL',
      py_modules=['kiseru'])
