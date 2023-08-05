from distutils.core import setup


setup(name='spelltinkle',
      version='0.2.0',
      description='Terminal text editor',
      long_description=open('README.rst').read(),
      author='J. J. Mortensen',
      author_email='jj@smoerhul.dk',
      url='http://spelltinkle.org',
      packages=['spelltinkle', 'spelltinkle/test'],
      scripts=['bin/spelltinkle'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: ' +
          'GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Text Editors :: Text Processing'])
