from setuptools import setup

setup(name='steptoolkit',
	version='0.3',
	description='The unofficial Python toolkit of Step Logic Ltd',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development :: Libraries',
	],
	url='https://bitbucket.org/idrey/steptoolkit',
	author='Ilya Drey',
	author_email='ilya@drey.su',
	license='MIT',
	packages=['steptoolkit', 'steptoolkit.ccwtool'],
	package_data = {
		'steptoolkit.ccwtool': ['images/*.jpg'],
	},
	scripts=['bin/ccwtool-cli'],
	install_requires=[
		'xlsxwriter',
	],
	zip_safe=False)
