# encoding: utf-8, division
from __future__ import print_function, division

from setuptools import setup, find_packages

VERSION = (0, 0, 3)


setup(name="raw2mzml",
      version="%d.%d.%d" % VERSION,
      maintainer="Uwe Schmitt",
      maintainer_email="uwe.schmitt@id.ethz.ch",
      license="http://opensource.org/licenses/BSD-3-Clause",
      url="https://ssdmsource.ethz.ch/uweschmitt/raw2mzml/tree/master",
      platforms=["win32"],
      description='library and command line tool to convert Thermo Fisher raw files to mz(X)ML',
      long_description="""
`raw2mzml` is a Python package for wraping common use cases of `msconvert.exe`
commandline tool.

`msconvert.exe` is part of Proteowizard (<http://proteowizard.sourceforge.net/>)
and allows conversion from Thermo Fisher .raw files to open source formats
.mzML and .mzXML. It has many options and getting them right is not always easy and wrong usage
results in wrong conversion results. Instead `raw2mzml` has only a configurable options which
cover common use cases.

Beyond the package it ships with a command line tool having the same name.
After installation you might run

    $ raw2mzml --help

to learn about its usage.
""",

      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,   # see MANIFEST.in
      zip_safe=False,
      install_requires=['Click>=6.0'],
      entry_points={
           'console_scripts':
           [
               'raw2mzml = raw2mzml.main:main',
           ]
      },

      )
