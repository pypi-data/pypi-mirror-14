import re
from setuptools import setup, find_packages

with open('spelltinkle/__init__.py') as fd:
    version = re.search("__version__ = '(.*)'", fd.read()).group(1)

with open('README.rst') as fd:
    long_description = fd.read()
    
setup(name='spelltinkle',
      version=version,
      description='Terminal text editor',
      long_description=long_description,
      author='J. J. Mortensen',
      author_email='jj@smoerhul.dk',
      url='http://spelltinkle.org',
      packages=find_packages(),
      install_requires=['pygments', 'pep8', 'pyflakes'],
      entry_points={'console_scripts': ['spelltinkle = spelltinkle.run:run']},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: '
          'GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Text Editors :: Text Processing'])
