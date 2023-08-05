from setuptools import setup, find_packages
from extro import __version__

with open('requirements.txt') as fd:
    requires = fd.read().splitlines()

setup(name='extro.py',
      author='Lars Kellogg-Stedman',
      author_email='lars@oddbit.com',
      url='https://github.com/larsks/extro.py',
      version=__version__,
      py_modules=['extro'],
      install_requires=requires,
      entry_points={'console_scripts': ['extropy = extro:main']})
