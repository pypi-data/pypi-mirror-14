from setuptools import setup

setup(
	name='interest-calc',
	version='0.0.1',
	description='Very simple tool to compute interest gains over time in the command line.',
	url='https://gitlab.com/PedroSilva/interest',
	author='Pedro Silva',
	author_email='ams.pedro@gmail.com',
	license='MIT',
	packages=['interest'],
	scripts=['bin/interest-calc'],
	zip_safe=False
)
