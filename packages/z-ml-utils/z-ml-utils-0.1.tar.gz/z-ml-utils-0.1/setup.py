from setuptools import setup

setup(name='z-ml-utils',
      version='0.1',
      description='A collection of machine learning functions for Python model making',
      url='http://github.com/zthoutt/ml-utils',
      author='Zack Thoutt',
      author_email='zackarey.thoutt@colorado.edu',
      license='MIT',
      packages=['zmodel'],
      install_requires=[
          'xgboost',
          'sklearn',
      ],
      zip_safe=False)
