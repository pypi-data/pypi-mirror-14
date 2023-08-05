from setuptools import setup, find_packages
with open('README.rst') as f:
    readme = f.read()

setup(name='FunnyBonesProject',
      version='1.0.2',
      author='Abhijit Baxi',
      author_email='baxiabhijit@gmail.com',
      license='MIT',
      description='Example package that tells a joke',
      long_description=readme,
      packages=find_packages())