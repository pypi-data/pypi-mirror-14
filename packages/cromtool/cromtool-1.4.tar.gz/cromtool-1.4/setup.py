from setuptools import setup

version = '1.4'
long_description = 'Development tool for Cromwell'

setup(
  name='cromtool',
  version=version,
  description=long_description,
  author='Scott Frazer',
  author_email='scott.d.frazer@gmail.com',
  packages=['cromtool'],
  package_dir={'cromtool': 'cromtool'},
  install_requires=[
      "xtermcolor",
      "requests",
      "pygments",
      "arrow",
      "google-api-python-client"
  ],
  scripts={
      'scripts/cromtool',
  },
  license = 'MIT',
  url = "http://github.com/broadinstitute/cromwell",
  classifiers=[
      'License :: OSI Approved :: MIT License',
      "Programming Language :: Python",
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Natural Language :: English"
  ]
)
