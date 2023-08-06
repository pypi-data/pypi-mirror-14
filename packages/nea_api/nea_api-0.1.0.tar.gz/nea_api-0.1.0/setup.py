from setuptools import setup
setup(
  name = 'nea_api',
  packages = ['nea_api'], # this must be the same as the name above
  version = '0.1.0',
  install_requires=[
        'xmltodict','requests'
  ],
  description = "Python Wrapper for NEA.gov.sg's Data API",
  author = 'David Chua',
  author_email = 'zhchua@gmail.com',
  url = 'https://github.com/davidchua/nea_api', # use the URL to the github repo
  download_url = 'https://github.com/davidchua/nea_api/tarball/0.1.0', # I'll explain this in a second
  keywords = ['data.gov.sg', 'python', 'wrapper', 'psi', 'singapore'], # arbitrary keywords
  classifiers = [],
)
