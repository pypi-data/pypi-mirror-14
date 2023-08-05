#import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "lcse",
    version = "9.0.1",
    author = "Stou Sandalski",
    author_email = "sandalski@astro.umn.edu",
    description = ("Python modules for reading formats produced by LCSE codes"),
    license = "Apache",
    keywords = "ppmstar cfd lut keys rprofile restart bob anp",
    url = "http://lcse.umn.edu/",
    packages=['lcse'],
    install_requires=['numpy'],
#    long_description=read('README'),
#    classifiers=[
#        "Development Status :: 3 - Alpha",
#        "Topic :: Libraries",
#    ],
)
