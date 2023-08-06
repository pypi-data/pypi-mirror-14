from setuptools import setup

import glob

setup(
    name = 'osex',
    packages = ['osex'],
    version = '0.3.2',
    description = 'extension for python\'s build-in operating system interface',
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://github.com/fphammerle/osex',
    download_url = 'https://github.com/fphammerle/osex/tarball/0.3.2',
    keywords = [],
    classifiers = [],
    scripts = glob.glob('scripts/*'),
    install_requires = ['ioex>=0.3'],
    tests_require = ['pytest']
    )
