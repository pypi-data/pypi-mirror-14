import os
from setuptools import setup, find_packages

version = '0.0.3'

long_description = \
    open(os.path.join("docs", "source", "README.rst")).read() + "\n" + \
    open(os.path.join("docs", "source", "HISTORY.rst")).read()

setup(name='mr.kangaroo',
      version=version,
      description="mr.kangaroo",
      long_description=long_description,
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='kangaroo',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/mr.kangaroo',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
