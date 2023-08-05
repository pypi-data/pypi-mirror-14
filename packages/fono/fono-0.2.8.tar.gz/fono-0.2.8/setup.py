from setuptools import setup
import sys
import fono
from os import path

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()

from pip.req import parse_requirements
install_requires = [str(ir.req) for ir in parse_requirements(path.join(here, 'requirements.txt'), session=False)]

setup(
    name=fono.__title__,
    version=fono.__version__,

    description=fono.__summary__,
    long_description=long_description,
    license=fono.__license__,
    url=fono.__uri__,

    author=fono.__author__,
    author_email=fono.__email__,

    packages=["fono", "fono.data"],

    entry_points={
        "console_scripts": [
            "fono = fono.run:main",
        ],
    },

    install_requires=install_requires,

    # dependency_links=[
        # "git+ssh://git@github.com/kdheepak89/click.git@7.0#egg=click-7.0"
    # ]
)
