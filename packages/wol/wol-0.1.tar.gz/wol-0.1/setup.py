import wol
from distutils.core import setup
setup(
  name = 'wol',
  packages = ['wol'], # this must be the same as the name above
  version = '0.1',
  description = 'instant query from wolframalpha',
  author = 'Manoj Pandey',
  author_email = 'manojpandey1996@gmail.com',
  url = 'https://github.com/manojpandey/hackinthenorth/tree/wol', # use the URL to the github repo
  download_url = 'https://github.com/manojpandey/hackinthenorth/archive/wol.zip', # I'll explain this in a second
  keywords = ['wolframalpha', 'command-line', 'terminal', 'query'], # arbitrary keywords
  classifiers = [],
  entry_points={
    'console_scripts': [
      'wol = wol.wol:wol_cli',
    ]
    },
  install_requires=[
    'wolframalpha'
  ],
)