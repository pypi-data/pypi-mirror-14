import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-jquery',
    version='1.12.2',
    url="http://bitbucket.org/massimilianoravelli/django-jquery",
    description='jQuery packaged in an handy django app to speed up new applications and deployment.',
    long_description=long_description,
    author='Massimiliano Ravelli',
    author_email='massimiliano.ravelli@gmail.com',
    license='MIT',
    keywords='django jquery staticfiles'.split(),
    platforms='any',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    zip_safe=False,
    packages=find_packages(),
    package_data={'jquery': ['static/js/*.js']},
    install_requires=requirements,
)
