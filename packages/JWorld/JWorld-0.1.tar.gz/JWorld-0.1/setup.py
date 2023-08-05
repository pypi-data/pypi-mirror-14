from ez_setup import use_setuptools 
use_setuptools()
from setuptools import setup, find_packages
setup(
    name = "JWorld",
    version = "0.1",
    packages = find_packages(),
    scripts = ['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],
    #package_data = {'': ['data/*.xml’]}, #
    package_data = {'JWorld':['data/*.xml'],
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    dependency_links= [
        "http://peak.telecommunity.com/snapshots/"
    ],
    # metadata for upload to PyPI
    author = "Me",
    author_email = "me@example.com",
    description = "This is an Example Package",
    license = "PSF",
    keywords = "hello world example examples",
    url = "http://example.com/HelloWorld/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.

    entry_points={
        'console_scripts': [
            'foo = my_package.some_module:main_func',
            'bar = other_module:some_func',
        ],
        'gui_scripts': [
            'baz = my_package_gui:start_func',
        ],
        'setuptools.installation': [
            'eggsecutable = my_package.some_module:main_func',
        ]
    }

)
