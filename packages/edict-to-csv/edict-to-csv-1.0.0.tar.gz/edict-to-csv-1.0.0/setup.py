#!/usr/bin/env python3

""" Setup script for packaging and installation. """

from distutils.core import setup

with open('README.rst', 'r', encoding='utf-8') as fin:
    LONG_DESCRIPTION = fin.read()

setup(
    #
    # Basic information
    #
    name='edict-to-csv',
    version='1.0.0',
    author='yaoguai',
    author_email='lapislazulitexts@gmail.com',
    url='https://github.com/yaoguai/edict-to-csv',
    license='MIT',
    #
    # Descriptions & classifiers
    #
    description='Convert the EDICT dictionary format into CSV.',
    long_description=LONG_DESCRIPTION,
    keywords='asia cedict chinese cjk csv dictionary edict japanese language',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Religion',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities'],
    #
    # Included Python files
    #
    scripts=[
        'cedict-to-csv',
        'edict1-to-csv'],
    py_modules=[
        'cedict_to_csv',
        'edict1_to_csv'],
    data_files=[
        ('share/doc/edict-to-csv', [
            'LICENSE.rst',
            'README.rst']),
        ('share/man/man1', [
            'cedict-to-csv.1',
            'edict1-to-csv.1'])]
)
