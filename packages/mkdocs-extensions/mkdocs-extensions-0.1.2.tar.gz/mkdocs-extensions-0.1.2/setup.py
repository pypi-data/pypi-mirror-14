# coding=utf8

from setuptools import setup, find_packages


setup(
    name='mkdocs-extensions',
    version='0.1.2',

    author='Duan Hongyi',
    author_email='duanhongyi@doopai.com',

    url='https://github.com/duanhongyi/mkdocs-slugify',
    description='Python mkdocs extensions',

    packages=find_packages(),
    install_requires=[
        'awesome-slugify',
    ],

    license='GNU GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='slugify slug transliteration russian german unicode translation flexible',
)
