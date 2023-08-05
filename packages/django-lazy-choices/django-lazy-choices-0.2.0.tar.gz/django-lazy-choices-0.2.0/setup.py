#!/usr/bin/env python
import glob
import os
import re

from setuptools import find_packages, setup


def get_version(package):
    init_py = open(os.path.join('src', package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name='django-lazy-choices',
    version=get_version('lazychoices'),
    url='https://github.com/jamieconnolly/django-lazy-choices',
    author='Jamie Connolly',
    author_email='jamie@jamieconnolly.com',
    description='Lazy choices for Django models',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob.glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.8,<1.10'],
    extras_require={
        'dev': [
            'flake8>=2.5,<2.6',
            'isort>=4.2,<4.3',
        ]
    },
    keywords=['django'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='runtests.runtests',
)
