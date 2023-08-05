from setuptools import setup


setup(name='CGEA',
      version='0.903',
      description='Chemo Genomic Enrichment Analysis',
      url='https://bitbucket.org/MaxTomlinson/cgea',
      author='Max Tomlinson / Ben Readhead',
      author_email='max.tomlinson@mssm.edu',
      license='MIT',
      packages=['CGEA'],
      install_requires=[
          'pip>=8.1.1',
          'jsonpickle',
          'numpy',
          'scikit-learn',
          'scipy',
          'statsmodels',
          'pandas'
      ],
      include_package_data=True,
      zip_safe=False)


