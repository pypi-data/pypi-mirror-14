from setuptools import setup, find_packages
from tergraw.info import __version__, __name__


setup(
    name = __name__,
    version = __version__,
    packages = find_packages(),

    author = "lucas",
    author_email = "lucas.bourneuf@laposte.net",
    description = "Draw graphs in terminal",
    long_description = open('README.mkd').read(),
    keywords = "graph terminal draw",
    url = "https://github.com/Aluriak/tergraw",

    classifiers = [
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
