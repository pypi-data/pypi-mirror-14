# -*- coding: utf-8 -*-

"""
mekk.fics setup
"""

from setuptools import setup, find_packages
import os, sys
exec(open(os.path.join(os.path.dirname(__file__), "src", "mekk", "fics", "version.py")).read())

long_description = open("README.txt").read()

classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
    "License :: OSI Approved :: Artistic License",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    ]

license = "Artistic" # or MPL 1.1

requirements = [
    'six>=1.4.1',
]
if sys.version_info < (2,7,0):
    requirements.append('ordereddict')
if sys.version_info > (3,0,0):
    requirements.append('Twisted>=13.2.0')
else:
    requirements.append('Twisted')

setup(name='mekk.fics',
      version=VERSION,
      description="FICS client library.",
      long_description=long_description,
      classifiers=classifiers,
      keywords='FICS, chess',
      author='Marcin Kasperski',
      author_email='Marcin.Kasperski@mekk.waw.pl',
      url='http://bitbucket.org/Mekk/mekk.fics/',
      license=license,
      package_dir={'':'src'},
      packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['mekk'],
      test_suite = 'nose.collector',
      include_package_data = True,
      zip_safe=False,
      install_requires=requirements,
      tests_require=[
        'nose',
        'dict_compare',
      ]
)
