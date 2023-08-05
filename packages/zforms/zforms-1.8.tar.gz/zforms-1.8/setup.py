from distutils.core import setup

setup(name='zforms',
	version='1.8',
	url='https://github.com/sc4reful/zforms',
	license='MIT',
	author='sc4reful',
	author_email='4b1a2059@opayq.com',
	description='Tiny Flask form validation library.',
	packages=['zforms'],
	zip_safe=False,
	platforms='any',
	install_requires=['Flask', 'Pillow'],
	classifiers = [
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Development Status :: 5 - Production/Stable',
		'Framework :: Flask',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
)