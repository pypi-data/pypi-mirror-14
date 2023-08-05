#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Mon 12 Oct 2015 22:32:22 CEST

from setuptools import setup, dist

dist.Distribution(dict(setup_requires=['bob.extension']))

from bob.extension.utils import load_requirements, find_packages

install_requires = load_requirements()

# Define package version
version = open("version.txt").read().rstrip()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='bob.db.avspoof_btas2016',
    version=version,
    description='Audio AVspoof Attack Database Access API for BTAS 2016 Speaker Anti-spoofing Competition',
    url='http://github.com/bioidiap/bob.db.avspoof_btas2016',
    license='GPLv3',
    author='Pavel Korshunov',
    author_email='pavel.korshunov@idiap.ch',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requires,



    entry_points={
        'console_scripts': [
            'debug_avspoof_btas2016 = bob.db.avspoof_btas2016.debug_avspoof:main',
        ],
        # bob database declaration
        'bob.db': [
            'avspoof_btas2016 = bob.db.avspoof_btas2016.driver:Interface',
        ],

        # antispoofing database declaration
        'antispoofing.utils.db': [
            'avspoof_btas2016 = bob.db.avspoof_btas2016.spoofing:Database',
        ],

        # verification database declaration
        'bob.db.verification.utils': [
            'avspoof_btas2016-verify = bob.db.avspoof_btas2016.verification:Database',
        ],
    },

    classifiers=[
        'Framework :: Bob',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Database :: Front-Ends',
    ],
)
