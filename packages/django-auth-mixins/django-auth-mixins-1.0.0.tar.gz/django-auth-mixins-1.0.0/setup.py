from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Load README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-auth-mixins',
    version='1.0.0',

    description='Backport of Django 1.9 auth mixins.',
    long_description=long_description,

    url='https://github.com/dbrgn/django-auth-mixins/',

    author='Danilo Bargen',
    author_email='mail@dbrgn.ch',

    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='django mixins backport backports 1.8 1.9 auth',

    packages=['auth_mixins'],
    package_data={
        '': ['README.md', 'LICENSE'],
    },
)
