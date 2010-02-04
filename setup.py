#!/usr/bin/env python

from distutils.core import setup

def get_description():
    import os
    return ''.join(
        file(
            os.path.join(os.path.dirname(os.path.normpath(__file__)),
            'README.md'
        ), 'r').readlines()
    )

setup(
    name='django-legacy',
    version='0.1',

    license='New BSD License',

    author='Alex Koshelev',
    author_email='daevaorn@gmail.com',

    url='http://github.com/daevaorn/django-legacy/',

    packages=[
        'legacy',
    ],

    description='`django-legacy` provides the smart way '
                'to overwrite your legacy project urls',
    long_description=get_description(),

    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ]
)
