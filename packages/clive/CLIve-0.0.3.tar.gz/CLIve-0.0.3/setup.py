from distutils.core import setup

setup(
    name='CLIve',
    version='0.0.3',
    author='Sven Steinbauer',
    author_email='sven@unlogic.co.uk',
    maintainer='Sven Steinbauer',
    packages=['clive'],
    scripts=['bin/clive'],
    url='https://github.com/Svenito/clive',
    license='MIT',
    description='Follow Reddit live feeds from your terminal.',
    long_description=open('README.md').read(),
    install_requires=[
		"colorama (==0.3.7)",
		"html (==1.16)",
		"requests (==2.9.1)",
		"six (==1.10.0)",
		"websocket (==0.35.0)"
    ],
)
