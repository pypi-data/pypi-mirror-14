from setuptools import setup, find_packages

setup(name='mystiko',
      version='0.1',
      description='Collect kubernetes secrets into a python dictionary.',
      url='http://github.com/lander2k2/mystiko',
      author='Richard Lander',
      author_email='lander2k2@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)

