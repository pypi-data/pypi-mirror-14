from distutils.core import setup
setup(
  name = 'Exode',
  packages = ['Exode'],
  package_data={'Exode': ['Board/*.py','Core/*.py','Object/*.py']},
  install_requires=['pyserial'],
  version = '0.4.0',
  description = 'Exode is a Pythons library for communication between Arduino microcontroller boards and a connected computer.',
  author = 'Lenselle Nicolas',
  author_email = 'lenselle.nicolas@gmail.com',
  url = 'https://github.com/sne3ks/Exode',
  download_url = 'https://github.com/sne3ks/Exode/tarball/0.4',
  license='APACHE 2.0'
)

# python setup.py register
# python python setup.py sdist upload
# http://peterdowns.com/posts/first-time-with-pypi.html
