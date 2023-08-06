try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = 'dataloader',
      version='2.0',
      description='Implements a general purpose data loader for python non-sequential machine learning tasks. Part of the antk toolkit.',
      url='http://aarontuor.xyz',
      author='Aaron Tuor',
      author_email='tuora@students.wwu.edu',
      license='none',
      packages=['dataloader'],
      zip_safe=False)
