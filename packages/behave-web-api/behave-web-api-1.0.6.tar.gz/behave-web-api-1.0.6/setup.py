from setuptools import setup
import behave_web_api

long_description = open('README.rst', 'r').read()

setup_requires = ['wheel']

install_requires = [
    'behave>=1.2.4',
    'requests>=2.0.0',
    'ordereddict==1.1'
]


setup(
    name='behave-web-api',
    version=behave_web_api.__version__,
    packages=['behave_web_api', 'behave_web_api.steps'],
    setup_requires=setup_requires,
    install_requires=install_requires,
    description="Provides testing for JSON APIs with Behave",
    long_description=long_description,
    url='https://github.com/jefersondaniel/behave-web-api',
    author='Jeferson Daniel',
    author_email='jeferson.daniel412@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
