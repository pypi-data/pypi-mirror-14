from setuptools import setup, find_packages


def read(filename):
    f = open(filename)
    text = f.read()
    f.close()
    return text

setup(
    name=u'pysword',
    version=u'0.2.1',
    packages=find_packages(exclude=[u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
    url=u'https://gitlab.com/tgc-dk/pysword',
    license=u'GPL2',
    author=u'Tomas Groth',
    author_email=u'tomasgroth@yahoo.dk',
    description=u'A native Python2/3 reader module for the SWORD Project Bible Modules',
    long_description=read(u'README.rst'),
    platforms=[u'any'],
    classifiers=[
        u'Development Status :: 3 - Alpha',
        u'Intended Audience :: Religion',
        u'Intended Audience :: Developers',
        u'Operating System :: OS Independent',
        u'Programming Language :: Python :: 2',
        u'Programming Language :: Python :: 3',
        u'Topic :: Religion',
        u'Topic :: Software Development',
        u'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
)
