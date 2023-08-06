import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

requires = [
    'cssselect',
    'lxml',
    'requests'
]

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='middlebury-directory',
    version='1.0.0',
    packages=['directory'],
    include_package_data=True,
    license='MIT',
    description='A Python API for the Middlebury directory.',
    long_description=README,
    url='https://github.com/coursereviews/directory',
    install_requires=requires,
    author='Dana Silver',
    author_email='dsilver@middlebury.edu',
    keywords='directory middlebury search people',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
