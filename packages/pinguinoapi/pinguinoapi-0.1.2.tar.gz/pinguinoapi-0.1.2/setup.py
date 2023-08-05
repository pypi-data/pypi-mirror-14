#!/usr/bin/env python

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 22/10/15
"""

from setuptools import setup, find_packages

setup(name = "pinguinoapi",
      version = "0.1.2",
      packages = find_packages(),
      include_package_data=True,
      description = "Pinguino API module",
      description_file = "README.rst",

      author = "Yeison Cardona",
      author_email = "yeisoneng@gmail.com",
      maintainer = "Yeison Cardona",
      maintainer_email = "yeisoneng@gmail.com",

      # url = "https://bitbucket.org/YeisonEng/bitcoinmod",
      # download_url = "https://bitbucket.org/YeisonEng/bitcoinmod/downloads",

      license = "BSD 3-Clause",
      install_requires = ["requests",],
      keywords = 'pinguino',

      classifiers=[#list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers

                   ],
      )
