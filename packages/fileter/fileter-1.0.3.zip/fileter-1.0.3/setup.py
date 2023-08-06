from distutils.core import setup
setup(
  name = 'fileter',
  packages = ['fileter'],
  package_data = {'fileter' : ["filters/*.py", "iterators/*.py", "sources/*.py"] },
  version = '1.0.3',
  description = 'Lightweight python lib to iterate files and directories with smart filters.',
  author = 'Ronen Ness',
  author_email = 'ronenness@gmail.com',
  url = 'https://github.com/RonenNess/Fileter',
  download_url = 'https://github.com/RonenNess/Fileter/tarball/1.0.3',
  keywords = ['files', 'directories', 'iteration', 'process files', 'filters', 'walk'],
  classifiers = [],
)