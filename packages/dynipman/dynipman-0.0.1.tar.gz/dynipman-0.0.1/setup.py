from distutils.core import setup
VERSION = '0.0.1'
setup(
  name = 'dynipman',
  install_requires = ['tornado'],
  packages = ['dynipman',],
  package_data = {'dynipman':['scripts/*',]},
  scripts = ['dynipman/scripts/dynipman_cd','dynipman/scripts/dynipman_sd',],
  version = VERSION,
  description = 'Personal IP address name service for Developers who move around a lot',
  author = 'Kumseok Jung',
  author_email = 'jungkumseok@gmail.com',
  license = 'LICENSE.txt',
  url = 'https://github.com/jungkumseok/dynipman',
  download_url = 'https://github.com/jungkumseok/dynipman/archive/'+VERSION+'.tar.gz',
  keywords = ['remote', 'ip address', 'dns'], 
  classifiers = [],
)