#query_phenomizer#

A small module for querying the [phenomizer tool](http://compbio.charite.de/phenomizer/) with HPO-terms.

## Installation ##

    pip install query_phenomizer

or
    
    git clone https://github.com/moonso/query_phenomizer.git
    cd query_phenomizer
    python setup.py install

##Usage##

    query_phenomizer --hpo_term HP:0001623 --hpo_term HP:0002465 --output genes.txt

