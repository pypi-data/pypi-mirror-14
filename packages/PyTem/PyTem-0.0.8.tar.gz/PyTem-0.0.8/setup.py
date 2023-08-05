from distutils.core import setup
setup(
    name = "PyTem",
    py_modules=['pytem'],
    version = "0.0.8",
    description = "Python-Server-Pages-like Templates",
    author = "Steve Beisner",
    author_email = "beisner@alum.mit.edu",
    url = "https://github.com/stevebeisner/PyTem",
    download_url = "https://github.com/stevebeisner/PyTem/archive/master.zip",
    keywords = ["templates", "python server pages"],
    classifiers = [
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing"
        ],
    long_description = """\
PyTem Template Engine
---------------------
 - Requires Python >= 3
 - Small (single file) and simple Python-Server-Pages-like template engine.
 - Run from the command line,
 - OR can be imported into another Python 3 program.
"""
)

