from setuptools import setup, find_packages

setup(name='gtimes',
      version='0.1',
      description='Time and date modules capable of handling GPS time',
      url='http://github.com/imo/gtimes',
      author='Benedikt G. Ofeigsson',
      author_email='bgo@vedur.is',
      license='Icelandic Met Office',
      package_dir={'gtimes': 'gtimes'},
      install_requres=['pytz','dateutils'],
      scripts=['timecalc'],
      packages=find_packages(),
      zip_safe=False)
