from os import path
import sys

here = path.abspath(path.dirname(__file__))

from pip.req import parse_requirements


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()

version = sys.version_info[:2]
if version < (2, 7):
    print('fono requires Python version 2.7 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)
elif (3, 0) < version:
    print('fono requires Python version 3.3 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)

VERSION = '0.1.3'

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(path.join(here, 'requirements.txt'), session=False)
# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

extras_require = {":sys_platform=='win32'": ['win_unicode_console']}

from distutils.core import setup
setup(
  name = 'fono',
  packages = ['fono'], # this must be the same as the name above
  version = VERSION,
  description = 'A python package to find optimal number of orders',
  long_description=long_description,
  author = 'Dheepak Krishnamurthy',
  author_email = 'kdheepak89@gmail.com',
  url = 'https://github.com/kdheepak89/fono', # use the URL to the github repo
  download_url = 'https://github.com/kdheepak89/fono/tarball/0.1', # I'll explain this in a second
  keywords = ['pyomo', 'operations'], # arbitrary keywords
  license = ['Revised BSD License'],
  install_requires = reqs,
  extras_require = extras_require,
  entry_points={'console_scripts': [
              'fono = fono.run:main',
              ]},
  classifiers = [],
)
