from setuptools import setup, find_packages

setup(
  name = 'homework-qingcloud-cli',
  version = 0.6,
  packages = find_packages('.'),
  install_requires = ['requests','PyYAML>=3.1'],
  entry_points = {
    'console_scripts': [
      'homework-qingcluod-cli = action.driver:main']
  },

  author = 'phantooom',
  author_email = 'zouruixp@sina.com',
  description = 'homework-qingcluod-cli',
  license = 'MIT',
  keywords = 'homework',
  url = 'http://fullstack.love',
  package_dir = {'homework-qingcluod-cli': 'action'},
)