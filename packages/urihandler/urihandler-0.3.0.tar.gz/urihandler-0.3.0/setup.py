import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'PyYAML'
    ]

setup(name='urihandler',
      version='0.3.0',
      description='A tiny application that handles (cool) uri\'s.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='https://github.com/OnroerendErfgoed/urihandler',
      license='GPLv3',
      keywords='web wsgi pyramid uri',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='urihandler',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = urihandler:main
      """,
      )
