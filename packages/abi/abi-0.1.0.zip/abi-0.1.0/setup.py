from setuptools import setup

setup(name='abi',
      version='0.1.0',
      description='DLL ABI loader',
      url='http://github.com/oakfang/abi',
      install_requires={
        'cffi>=1.5.2'
      },
      author='Alon Niv',
      author_email='oakfang@gmail.com',
      license='MIT',
      packages=['abi'])