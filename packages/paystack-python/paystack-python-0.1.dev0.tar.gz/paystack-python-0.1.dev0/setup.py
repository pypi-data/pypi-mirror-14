try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(name = 'paystack-python',
      cmdclass={'build_py': build_py},
      version = '0.1dev',
      packages = ['paystack',],
      long_description = 'Paystack python library',
      url= 'https://github.com/dayoreke/paystack-python',
      author='Adedayo Oluokun ',
      author_email='dayoreke@gmail.com',
      install_requires = 'requests >= 0.8.8',
      test_suite='paystack.test.all',
      tests_require=['unittest2'],
      )