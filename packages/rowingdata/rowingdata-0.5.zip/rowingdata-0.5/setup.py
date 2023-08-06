from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
	return f.read()

setup(name='rowingdata',

      version='0.5',

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
	  'mechanize'
	  ],

      zip_safe=False)
