from __future__ import unicode_literals

from setuptools import find_packages, setup


def get_version(filename):
    from re import findall
    with open(filename) as f:
        metadata = dict(findall("__([a-z]+)__ = '([^']+)'", f.read()))
    return metadata['version']


setup(
    name='Mopidy-Podcast-iTunes',
    version=get_version('mopidy_podcast_itunes/__init__.py'),
    url='https://github.com/tkem/mopidy-podcast-itunes',
    license='Apache License, Version 2.0',
    author='Thomas Kemmer',
    author_email='tkemmer@computer.org',
    description=(
        'Mopidy extension for searching and browsing podcasts '
        'on the Apple iTunes Store'
    ),
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.1',
        'Mopidy-Podcast >= 2.0',
        'Pykka >= 1.1',
        'requests >= 2.0'
    ],
    entry_points={
        'mopidy.ext': [
            'podcast-itunes = mopidy_podcast_itunes:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
