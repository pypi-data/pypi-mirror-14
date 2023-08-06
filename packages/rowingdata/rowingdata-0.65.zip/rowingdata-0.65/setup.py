from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
	return f.read()

setup(name='rowingdata',

      version='0.65',

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

      scripts=[
	  'bin/crewnerdplot.py',
	  'bin/painsledplot.py',
	  'bin/tcxtoc2.py',
	  'bin/painsledtoc2.py',
	  'bin/painsled_desktop_plot.py',
	  'bin/painsled_desktop_toc2.py',
	  'bin/painsledplottime.py',
	  'bin/painsled_desktop_plottime.py',
	  'bin/crewnerdplottime.py',
	  'bin/roweredit.py',
	  ]

      )
