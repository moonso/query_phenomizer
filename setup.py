try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="query_phenomizer",
    version="0.3",
    description = "Tool for query and parsing the phenomizer tool",
    # long_description = open( "README.md", "r" ).read( ),
    install_requires = [
        'click', 
        'requests',
    ],
    packages = [
        'query_phenomizer', 
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and
    # allow pip to create the appropriate form of executable for the
    # target platform.
    entry_points=dict(
        console_scripts=[
            'query_phenomizer = query_phenomizer.__main__:cli',
        ],
    ),
    license="Modified BSD",
    url="https://www.github.com/moonso/query_phenomizer",
    author = 'Mans Magnusson',
    author_email = 'mans.magnusson@scilifelab.se',
)
