from setuptools import setup
import os

cwd = os.path.dirname(os.path.realpath(__file__))

try:
   import pypandoc
   long_description = pypandoc.convert(cwd + '/README.md', 'rst')
except (IOError, ImportError):
   try:
      long_description = open(cwd + '/README.md').read()
   except:
      long_description = 'Official Popily API client'

setup(name='popily-api',
      version='0.0.13',
      description='Official Python client for the Popily API',
      long_description=long_description,
      url='https://github.com/popily/popily-api',
      download_url ='https://github.com/ushahidi/geograpy/tarball/0.0.13',
      author='Jonathon Morgan',
      author_email='jonathon@popily.com',
      license='MIT',
      packages=['popily_api'],
      install_requires=[
            'requests',
      ],
      zip_safe=False)