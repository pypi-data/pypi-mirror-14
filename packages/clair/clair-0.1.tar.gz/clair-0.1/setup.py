import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'docker-py',
    'requests'
    ]

setup(name='clair',
      version='0.1',
      description='Import a Docker image layers to Clair for security analysis',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python"
        ],
      author='Olivier Sallou',
      author_email='olivier.sallou@irisa.fr',
      url='https://bitbucket.org/osallou/clair',
      keywords='docker clair',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires
      )
