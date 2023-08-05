from setuptools import setup

def readme():
	with open('README.rst') as f:
		return(f.read())

setup(name='surveyhelper',
	  version='0.1.1.dev3',
	  description="Survey package for reporting on survey data from Qualtrics.",
	  url="http://github.com/cwade/surveyhelper",
	  author="cwade",
	  author_email="pysurveyhelper@gmail.com",
	  license='MIT',
	  packages=['surveyhelper'],
	  install_requires=['beautifulsoup4', 'pandas', 'jinja2', 'unidecode', 'scipy', 'pyyaml'],
	  zip_safe=False)
