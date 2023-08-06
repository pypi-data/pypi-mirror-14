from distutils.core import setup

setup(
  name = 'statement-extractor',
  packages = ['statement_extractor'],
  package_dir = {'statement_extractor': 'statement_extractor'},
  package_data = {'statement_extractor': ['prep/patterns/English.txt','tests/__init__.py','tests/test.py']},
  version = '0.5',
  description = 'Extracts statements from text',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/statement-extractor',
  download_url = 'https://github.com/DanielJDufour/statement-extractor/tarball/download',
  keywords = ['language','statements','parsing','python','tagging'],
  classifiers = [],
)
