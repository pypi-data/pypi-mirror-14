from setuptools import setup, find_packages
setup(
  name='jsonalyzer',
  license='MIT',
  version='0.0.3',
  url='https://github.com/saurabh-hirani/jsonalyzer',
  description=('Write callbacks for anlayzing json'),
  author='Saurabh Hirani',
  author_email='saurabh.hirani@gmail.com',
  packages=find_packages(),
  install_requires=[
    'click',
    'importlib',
    'simplejson',
    'requests'
  ],
  entry_points = {
    'console_scripts': [
      'jsonalyzer=jsonalyzer.cmdline:jsonalyzer',
    ]
  }
)
