import os
from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-jrac',
    version='1.0.2.dev10',
    url="https://github.com/daavve/django-jrac",
    description='jQuery Resize And Crop (jrac): visually resize an image and place a crop',
    long_description=long_description,
    author='David McInnis',
    author_email='davidm@eagles.ewu.edu',
    license='GPLv3+',
    keywords=('django', 'jquery', 'jrac'),
    platforms='any',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
    packages=['jrac'],
    package_data={'jrac': ['static/js/*.js',
                           'static/js/*.css',
                           'static/js/images/*.gif']},
    install_requires=[
        'django-jquery>=1.4.4',
        'django-jquery-ui>=1.8.7'
    ]
)
