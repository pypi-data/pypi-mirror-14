from setuptools import setup

setup(
	name='interest-calc',
	version='0.0.3',
	description='Very simple tool to compute interest gains over time in the command line.',
	url='https://gitlab.com/PedroSilva/interest',
	author='Pedro Silva',
	author_email='ams.pedro@gmail.com',
	license='MIT',
	packages=['interest'],
	scripts=['bin/interest-calc'],
	install_requires=[
		'docopt', 'toolz',
	],
	zip_safe=False
)
