from setuptools import setup

setup(name='entroport',
      version='0.1',
      description='portfolio allocation with relative entropy minimization',
      url='http://github.com/nuffe/entroport',
      author='nuffe',
      license='MIT',
      packages=['entroport'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

