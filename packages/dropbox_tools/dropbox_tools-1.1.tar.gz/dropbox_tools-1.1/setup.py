from setuptools import setup

setup(name ='dropbox_tools',
      version = '1.1',
      description = 'A collection of command line tools for Dropbox',
      url = 'http://github.com/agileronin/dropbox_tools',
      author = 'Gregory Mundy',
      author_email = 'greg.mundy@agileronin.com',
      license = 'MIT',
      packages = ['dropbox_tools'],
      install_requires = [
          'dropbox'
      ],
      zip_safe = False)

