import io
import os

from outlawg import __version__
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf8') as f:
    README = f.read()
with io.open(os.path.join(here, 'CHANGELOG'), encoding='utf8') as f:
    CHANGES = f.read()

extra_options = {
    'packages': find_packages(),
}


setup(name='outlawg',
      version=__version__,
      description='Not your grandmother\'s logging tool',
      long_description=README + '\n\n' + CHANGES,
      classifiers=['Topic :: Software Development :: Quality Assurance',
                   'Topic :: Software Development :: Testing',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4'
                   ],
      keywords='[logging, test]',
      author='Richard Pappalardo',
      author_email='rpappalax@gmail.com',
      license='MPL2',
      include_package_data=True,
      )
