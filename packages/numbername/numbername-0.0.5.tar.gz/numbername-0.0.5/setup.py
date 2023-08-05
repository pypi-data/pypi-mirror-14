from distutils.core import setup
setup(
    name = "numbername",
    packages = ["numbername"],
    version = "0.0.5",
    description = "Converts integers to number name",
    author = "Anand Mishra",
    author_email = "akm.inbox@hotmail.com",
    url = "https://github.com/anand-mishra/pynumbername",
    download_url =
"https://pypi.python.org/packages/source/n/numbername/numbername-0.0.5.tar.gz",
    keywords = ["encoding", "i18n", "xml"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
     long_description = """\
Installation
============

pip install numbername


Usage
=====


Convert integers to number name

    from numbername import to_number_name

    print to_number_name(1123) 

    #ouputs: one thousand one hundred and twenty three

Convert integers to comma placed number

    from numbername import to_comma_placed

    print to_number_name(1123)

    #outputs: 1,123

Limitations
===========

1. Works only with non-negative numbers
2. Works only with integers
"""    
)
