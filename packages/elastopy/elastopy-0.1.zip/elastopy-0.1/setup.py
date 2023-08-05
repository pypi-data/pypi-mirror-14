from setuptools import setup

setup(name='elastopy',
      version='0.1',
      description='Stead state linear elasticity problem',
      url='https://github.com/nasseralkmim/elastopy',
      download_url='https://github.com/nasseralkmim/elastopy/releases',
      author='Nasser Alkmim',
      author_email='nasser.alkmim@gmail.com',
      license='MIT',
      packages=['elastopy'],
      install_requires=[
          'numpy',
          'matplotlib',
          'networkx',
          'scipy'
      ],
      zip_safe=False)
