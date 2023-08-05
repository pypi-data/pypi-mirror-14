from setuptools import setup

setup(
    name='spotifytracker',
    version='0.0.7',
    packages=['spotify_tracker'],
    url='http://github.com/eriktaubeneck/spotifytracker',
    license='MIT',
    author='Erik Taubeneck',
    author_email='erik.taubeneck@gmail.com',
    description='Track your Spotify play history.',
    long_description=__doc__,
    py_modules=['spotify_tracker'],
    zip_safe=False,
    include_package_data=True,
    platforms='OS X',
    install_requires=[
        'pyyaml >=3.0, <4.a0',
        'docopt >=0.6.0, <0.7.0',
        'spotipy >=2.3.7, <2.4.0',
    ],
    entry_points="""
    [console_scripts]
    spotifytracker = runner:main
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English ',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
