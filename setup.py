from setuptools import setup

DIST_NAME = 'bio-sim'
AUTHOR = 'Will Asciutto'
AUTHOR_EMAIL = 'wjasciutto@gmail.com'
VERSION = '0.0.2'
DESCRIPTION = 'Simulates a simple, self-contained ecosystem'
URL = 'github.com:wasciutto/BioSim'
CLASSIFIERS = [ 'Intended Audience :: Developers',
                'Programming Language :: Python',
                'License :: MIT License',
                'Operating System :: OS Independent']
INSTALL_REQUIRES = [ 'matplotlib~=3.4.1',
                     'numpy~=1.20.2',
                     'click~=7.1.2',
                     'Flask~=1.1.2']

setup(name=DIST_NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      version=VERSION,
      description=DESCRIPTION,
      url=URL,
      classifiers=CLASSIFIERS,
      install_requires=INSTALL_REQUIRES)