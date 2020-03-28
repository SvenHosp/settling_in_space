"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

setup(
   name="custommagics",
   version="0.0.1",
   packages=find_packages(),
   install_requires=[
      'ipython'
   ],

   author="calisto107",
   description="custommagics v0.0.1",

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.yaml']
    }
)
