#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
VERSION = '0.1.1'
 
setup(name='podcastake',
      version=VERSION,
      description="download post cast according to the entry url",
      long_description='just enjoy',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python podcast download terminal',
      author='y10n',
      author_email='etng2004@gmail.com',
      url='https://github.com/etng/podcastake',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts':[
            'podcastake = podcastake.podcast:main'
        ]
      },
)
