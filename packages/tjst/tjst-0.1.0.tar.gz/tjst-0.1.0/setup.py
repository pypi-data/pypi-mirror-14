"""
tjst
--------

tjst = Tiny JavaScript Templating

Description:
  - High performance JS template engine.

It supports:
  - Anything you can write on JS =)
  - Server-side precompilation.
  - ...?

It not supports:
  - Templates inheritence.
  - Includes.
  - ...?

"""
from setuptools import setup

setup(
    name='tjst',
    version='0.1.0',
    author='David Kuryakin',
    author_email='me@dkuryakin.com',
    url='https://bitbucket.org/dkuryakin/tjst',
    download_url='https://bitbucket.org/dkuryakin/tjst/get/master.tar.gz',
    license='mit',
    description='Tiny JavaScript Templating.',
    keywords=['javascript', 'templates'],
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    test_suite="tjst.tests",
    include_package_data=True,
    packages=['tjst'],
    package_data={'tjst': ['*.js']},
    zip_safe=False,
    platforms='any',
    install_requires=['PyExecJS'],
    scripts=['tjst/bin/tjst-compile'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
