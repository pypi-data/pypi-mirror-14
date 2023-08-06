from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(	name='inspace',
		version='0.1',
		description= 'Jump into space with Nasa s photo of the day',
		long_description=readme(),
		author= 'RaddadZ',
		author_email= 'ananraddad@gmail.com',
		install_requires= [
			'BeautifulSoup'
		],
		keywords='space Nasa image day desktop wallpaper',
		url='http://github.com/RaddadZ/inspace',
		zip_safe=False
	 )



