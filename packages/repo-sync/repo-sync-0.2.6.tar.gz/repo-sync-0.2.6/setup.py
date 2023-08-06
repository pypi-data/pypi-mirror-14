from setuptools import setup

setup(
    name = "repo-sync",
    version = "0.2.6",
    author = "makefu",
    author_email = "github@syntax-fehler.de",
    description = ("Sync remotes to other remotes."),
    license = "MIT",
    keywords = " repo sync",
    url = "https://github.com/makefu/repo-sync",
    packages = ['reposync'],
    long_description = open('README.md').read(),
    classifiers = [
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    entry_points = {
        'console_scripts': ['repo-sync = reposync.cli:main'],
    },

    install_requires = [
        'GitPython>=1.0.1',
        'docopt',
    ]
)
