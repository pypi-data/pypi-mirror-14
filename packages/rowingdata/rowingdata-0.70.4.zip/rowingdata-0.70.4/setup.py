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
	  'rowingdata':[
	      '2016-03-25-0758.CSV',
	      '2016-03-25-0758.TCX',
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
	      'painsledplot = rowingdata.painsledplot',
	      'crewnerdplot = rowingdata.crewnerdplot.py',
	      'tcxtoc2 = rowingdata.tcxtoc2.py',
	      'painsledtoc2 = rowingdata.painsledtoc2.py',
	      'painsled_desktop_plot = rowingdata.painsled_desktop_plot.py',
	      'painsled_desktop_toc2 = rowingdata.painsled_desktop_toc2.py',
	      'painsledplottime = rowingdata.painsledplottime.py',
	      'painsled_desktop_plottime = rowingdata.painsled_desktop_plottime.py',
	      'crewnerdplottime = rowingdata.crewnerdplottime.py',
	      'roweredit = rowingdata.roweredit.py',
	      ]
	  },

      scripts=[
	  'bin/painsledplot2.py',
	  ]

      )
