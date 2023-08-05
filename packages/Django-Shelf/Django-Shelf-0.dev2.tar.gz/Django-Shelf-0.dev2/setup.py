#!/usr/bin/env python

from setuptools import find_packages, setup

DEV_TOOLS = [
    'selenium',
    'scripttest',
    'nose',
]

if __name__ == '__main__':
    setup(
        name='Django-Shelf',
        version='0.dev2',
        url='https://github.com/alexpirine/django-shelf',
        license='New BSD License',
        author='Alexandre Syenchuk',
        author_email='as@netica.fr',
        description='Django Framework with beautiful admin and CMS-like features',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Django >= 1.9',
        ],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Framework :: Django :: 1.9',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Internet :: WWW/HTTP :: WSGI',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: User Interfaces',
        ],
        tests_require = DEV_TOOLS,
        extras_require = {
            'dev': DEV_TOOLS,
        },
        test_suite = 'nose.collector',
    )
