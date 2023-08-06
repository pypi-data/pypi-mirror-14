from setuptools import setup
setup(
  name = 'nea_api',
  packages = ['nea_api'],
  version = '0.1.1',
  install_requires=[
        'xmltodict','requests'
  ],
  description = "Python Wrapper for NEA.gov.sg's Data API",
  author = 'David Chua',
  author_email = 'zhchua@gmail.com',
  url = 'https://github.com/davidchua/nea_api',
  download_url = 'https://github.com/davidchua/nea_api/tarball/0.1.1',
  keywords = ['data.gov.sg', 'python', 'wrapper', 'psi', 'singapore'],
  classifiers = [],
)
