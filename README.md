[![Build Status](https://travis-ci.org/moonso/query_phenomizer.svg)](https://travis-ci.org/moonso/query_phenomizer)
# query_phenomizer #

A small module for querying the [phenomizer tool](http://compbio.charite.de/phenomizer/) with HPO-terms.

# INFO!!! #

From 16/2-16 phenomizer demands a password and username when using the service in this way.
Request login credentials from sebastian.koehler@charite.de

## Installation ##

    pip install query_phenomizer

or
```
git clone https://github.com/moonso/query_phenomizer.git
cd query_phenomizer
pip install --editable .
```
##Usage##

    query_phenomizer HP:0001623 HP:0002465 --output phenitypes.txt

User can check if hpo terms exist by using the flag ```-c/--check_terms```.

    query_phenomizer HP:0001623 HP:02345555 --check_terms -v

Prints that HP:02345555 does not exist.

For more info run

    query_phenomizer --help
