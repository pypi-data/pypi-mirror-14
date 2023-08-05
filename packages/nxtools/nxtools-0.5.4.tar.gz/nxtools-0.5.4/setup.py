import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "nxtools",
    version = "0.5.4",
    author = "Martin Wacker",
    author_email = "martas@imm.cz",
    description = "Set of common utilities and little helpers.",
    license = "MIT",
    keywords = "utilities log logging ffmpeg watchfolder media mam time",
    url = "https://github.com/martastain/nxtools",
    packages=['nxtools', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Utilities",
    ],
)
