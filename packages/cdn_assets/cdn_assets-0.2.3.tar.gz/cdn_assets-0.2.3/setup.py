import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cdn_assets',
    version='0.2.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-tag-parser'],
    license='BSD License',  # example license
    description='Using CDN Assets(mainly JS and css) instead of downloading asset by your self.',
    long_description=README,
    url='https://github.com/lsc20051426/cdn-asserts',
    author='L',
    author_email='lsc20051426@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
)