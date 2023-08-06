import os
from setuptools import setup

from pip.req import parse_requirements
from pip.download import PipSession



def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

test_requirements = (
    [str(ir.req) for ir in
        parse_requirements('./requirements-dev.txt', session=PipSession())] +
    [str(ir.req) for ir in
        parse_requirements('./requirements-setup.txt', session=PipSession())]
)

setup(
    name='nonprimary-foreignkey',
    author='Lucas Wiman',
    author_email='lucas.wiman@gmail.com',
    packages=['nonprimary_foreignkey'],
    include_package_data=True,
    url='https://github.com/lucaswiman/nonprimary-foreignkey',
    license='Apache 2.0',
    description='Allows foreign-key prefetches on non-primary-key fields',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.md'),
    install_requires=[
        'Django>=1.7',
    ],
    tests_require=test_requirements,
    test_suite='runtests.runtests',
)
