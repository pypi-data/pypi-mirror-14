from setuptools import setup, find_packages
setup (
	name= "aboutdir",
	version = "1.0",
	description = 'Command line tool for adding description to directories',
	url = 'https://github.com/kousiksatish/about_directory',
	author = 'Kousik Satish',
	author_email = 'kousiksatish@gmail.com',

    packages = ['aboutdir'],

    entry_points = {
    	'console_scripts' : ['aboutdir=aboutdir:main']
    },
    keywords=['CLI', 'directory', 'aboutdir', 'about-directory', 'description-for-directory'],
    classifiers=[
	    'Programming Language :: Python :: 2',
	    'Programming Language :: Python :: 2.6',
	    'Programming Language :: Python :: 2.7',
	    'Programming Language :: Python :: 3',
	    'Programming Language :: Python :: 3.2',
	    'Programming Language :: Python :: 3.3',
	    'Programming Language :: Python :: 3.4',
	],
	)