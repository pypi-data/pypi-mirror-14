from setuptools import setup


import urllib, zipfile, os
from distutils.sysconfig import get_python_lib
def get_CGEA_data():
    package_path = get_python_lib()
    urllib.urlretrieve("https://bitbucket.org/MaxTomlinson/cgea/downloads/data.zip", 
                       package_path+"/CGEA/data.zip")
    zipfile.extractall(package_path+"/CGEA/data.zip")
    os.remove(package_path+"/CGEA/data.zip")

setup(name='CGEA',
      version='0.9',
      description='Chemo Genomic Enrichment Analysis',
      url='https://bitbucket.org/MaxTomlinson/cgea',
      author='Max Tomlinson',
      author_email='max.tomlinson@mssm.edu',
      license='MIT',
      packages=['CGEA'],
      install_requires=[
          'jsonpickle',
          'numpy',
          'scikit-learn',
          'scipy',
          'statsmodels',
          'pandas'
      ],
      cmdclass = {'my_command': get_CGEA_data},
      include_package_data=True,
      zip_safe=False)


