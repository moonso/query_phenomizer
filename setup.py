try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="query_phenomizer",
    version="0.2.1",
    description = "Tool for query and parsing the phenomizer tool",
    # long_description = open( "README.md", "r" ).read( ),
    install_requires = [
        'click', 
        'requests',
    ],
    packages = [
        'query_phenomizer', 
    ],
    scripts = [
        'scripts/query_phenomizer'
    ],
    license="Modified BSD",
    url="https://www.github.com/moonso/query_phenomizer",
    author = 'Mans Magnusson',
    author_email = 'mans.magnusson@scilifelab.se',
)
