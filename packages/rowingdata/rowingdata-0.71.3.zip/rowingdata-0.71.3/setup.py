from setuptools import setup, find_packages

import re

def readme():
    with open('README.rst') as f:
	return f.read()

setup(name='rowingdata',

      version=re.search(

	  '^__version__\s*=\s*"(.*)"',
	  open('rowingdata/rowingdata.py').read(),
	  re.M

	  ).group(1),

      description='The rowingdata library to create colorful plots from CrewNerd, Painsled and other rowing data tools',

      long_description=readme(),

      url='http://rowsandall.wordpress.com',

      author='Sander Roosendaal',

      author_email='roosendaalsander@gmail.com',

      license='MIT',

      packages=['rowingdata'],

      keywords = 'rowing ergometer concept2',
      
      install_requires=[
	  'numpy',
	  'scipy',
	  'matplotlib',
	  'pandas',
	  'mechanize',
	  'python-dateutil',
	  ],

      zip_safe=False,
      include_package_data=True,
      # relative to the rowingdata directory
      package_data={
	  'testdata':[
	      'crewnerddata.CSV',
	      'crewnerddata.tcx',
	      'example.csv',
	      'painsled_desktop_example.csv',
	      'RP_testdata.csv',
	      'testdata.csv'
	      ],
	  'bin':[
	      'testdata.csv',
	      'crewnerddata.csv',
	      'crewnerddata.tcx'
	      ],
	      
	  },

      entry_points = {
	  "console_scripts": [
	      'rowingdata = rowingdata.rowingdata:main',
	      'painsledtoc2 = rowingdata.painsledtoc2:main',
	      'painsledplot = rowingdata.painsledplot:main',
	      'crewnerdplot = rowingdata.crewnerdplot:main',
	      'tcxtoc2 = rowingdata.tcxtoc2:main',
	      'painsled_desktop_plot = rowingdata.painsled_desktop_plot:main',
	      'painsled_desktop_toc2 = rowingdata.painsled_desktop_toc2:main',
	      'painsledplottime = rowingdata.painsledplottime:main',
	      'painsled_desktop_plottime = rowingdata.painsled_desktop_plottime:main',
	      'crewnerdplottime = rowingdata.crewnerdplottime:main',
	      'roweredit = rowingdata.roweredit:main',
	      'copystats = rowingdata.copystats:main',
	      ]
	  },

      scripts=[
	  'bin/painsledplot2.py',
	  ]

      )
