import setuptools

import setuptools.command.test

import fuzzle

setuptools.setup(
    name='fuzzle',
    version=fuzzle.__version__,
    url='http://github.com/blazaid/fuzzle/',
    license='GNU General Public License v3',
    author='blazaid',
    tests_require=[],
    install_requires=[],
    author_email='alberto.da@gmail.com',
    description='A fuzzy controllers library for python',
    long_description=open('README.rst').read(),
    packages=['fuzzle', ],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
