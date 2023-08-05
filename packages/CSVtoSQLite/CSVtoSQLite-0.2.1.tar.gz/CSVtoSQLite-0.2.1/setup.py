from distutils.core import setup
setup(
  name = 'CSVtoSQLite',
  packages = ['CSVtoSQLite'], # this must be the same as the name above
  version = '0.2.1',
  description='Loads a CSV file a creates a preloaded SQLite database',
  author='Stanley Boakye',
  author_email='stan.boakye@gmail.com',
  url = 'https://github.com/maxifex/CSVtoSQLite', # use the URL to the github repo
  download_url = 'https://github.com/maxifex/CSVtoSQLite/tarball/0.1', # I'll explain this in a second
  keywords = ['csv', 'SQLite', 'convert'], # arbitrary keywords
  classifiers = [],
)
