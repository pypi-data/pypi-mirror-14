from distutils.core import setup
from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = []


def get_version(major=0, minor=0, build=0):
    return '%s.%s.%s' % (major, minor, build)


setup(
    name='virtenviro',
    version=get_version(
        major=0,
        minor=7,
        build=12
    ),
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    url='http://www.virtenviro.org/',
    license='GPL3',
    author='Kamo Petrosyan',
    author_email='kamo@haikson.com',
    description='Open source content management system (CMS) based on the django framework.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'django',
        'django-mptt',
        'django-filebrowser-no-grappelli',
        'lxml',
        'Pillow',
        'pytils',
        'sorl-thumbnail',
        'django-datetime-widget',
    ]
)
