from setuptools import setup

import glob

setup(
    name = 'jackin',
    # packages = ['jackin'],
    version = '0.1',
    description = '',
    author = 'Fabian Peter Hammerle',
    author_email = 'fabian.hammerle@gmail.com',
    url = 'https://github.com/fphammerle/jackin',
    download_url = 'https://github.com/fphammerle/jackin/tarball/0.1',
    keywords = [],
    classifiers = [],
    scripts = glob.glob('scripts/*'),
    install_requires = ['ioex>=0.3'],
    tests_require = ['pytest']
    )
