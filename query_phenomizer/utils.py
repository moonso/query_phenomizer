#!/usr/bin/env python
# encoding: utf-8
"""
query.py

query phenomizer and store the results in a ordered dictionary.

Created by Måns Magnusson on 2015-02-02.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""
from __future__ import print_function, unicode_literals

import sys
import os
import click
import requests

from pprint import pprint as pp



def parse_result(line):
    """
    Parse the result line of a phenomizer request.
    
    Arguments:
        line (str): A raw output line from phenomizer
    
    Returns:
         result (dict): A dictionary with the phenomizer info:
             {
                 'p_value': float,
                 'gene_id': str,
                 'omim_id': int,
                 'orphanet_id': int,
                 'decipher_id': int,
                 'any_id': int,
                 'mode_of_inheritance':str,
                 'description': str,
                 'raw_line': str
             }
             
    """
    result = {
        'p_value': None,
        'gene_id': None,
        'omim_id': None,
        'orphanet_id': None,
        'decipher_id': None,
        'mode_of_inheritance':None,
        'description': None,
        'raw_line': line
    }
    
    result_line = line.rstrip().split('\t')
    
    try:
        result['p_value'] = float(result_line[0])
    except ValueError:
        pass
    
    try:
        medical_litterature = result_line[2].split(':')
        if medical_litterature[0] == 'OMIM':
            result['omim_id'] = int(medical_litterature[1])
            result['any_id'] = int(medical_litterature[1])
        elif medical_litterature[0] == 'DECIPHER':
            result['decipher_id'] = int(medical_litterature[1])
            result['any_id'] = int(medical_litterature[1])
        elif medical_litterature[0] == 'ORPHANET':
            result['orphanet_id'] = int(medical_litterature[1])
            result['any_id'] = int(medical_litterature[1])
    except IndexError:
        pass
    
    try:
        description = result_line[3]
        result['description'] = description
    except IndexError:
        pass
    
    try:
        gene_id = result_line[4]
        result['gene_id'] = gene_id
    except IndexError:
        pass
    
    return result

def query(hpo_terms):
    """
    Query the phenomizer web tool
    
    Arguments:
        hpo_terms (list): A list with hpo terms
    
    Returns:
        parsed_terms (list): A list with the parsed HPO terms
     
    """
    
    parsed_terms = []
    
    basic_string = 'http://compbio.charite.de/phenomizer/phenomizer/PhenomizerServiceURI'
    questions = {'mobilequery':'true', 'terms':','.join(hpo_terms)}
    try:
        r = requests.get(basic_string, params=questions, timeout=10)
    except requests.exceptions.Timeout:
        print("The request timed out." ,
                file=sys.stderr)
        print("Exiting...",
                file=sys.stderr)
        sys.exit(1)
        
    if not r.status_code == requests.codes.ok:
        print("Phenomizer returned a bad status code: %s" % r.status_code,
                file=sys.stderr)
        print("Exiting...",
                file=sys.stderr)
        sys.exit(1)
    
    r.encoding = 'utf-8'
    
    for line in r.iter_lines():
        parsed_terms.append(parse_result(line))
    
    return(parsed_terms)

def validate_term(hpo_term):
    """
    Validate if the HPO term exists.
    
    Check if there are any result when querying phenomizer.
    
    Arguments:
       hpo_term (string): Represents the hpo term
    
    Returns:
        result (boolean): True if term exists, False otherwise
    
    """
    
    basic_string = 'http://compbio.charite.de/phenomizer/phenomizer/PhenomizerServiceURI'
    questions = {'mobilequery':'true', 'terms':hpo_term}
    result = True
    try:
        r = requests.get(basic_string, params=questions, timeout=10)
    except requests.exceptions.Timeout:
        result = False
        
    if not r.status_code == requests.codes.ok:
        result = False
    
    return result
    
@click.command()
@click.option('-t', '--hpo_term',
                multiple=True,
                help="Give hpo terms either on the form 'HP:0001623', or '0001623'"
)
@click.option('-c', '--check_terms',
                is_flag=True,
                help="Check if the term(s) exist"
)
def try_query(hpo_term, check_terms):
    if not hpo_term:
        print("Please specify at least one hpo term with '-t/--hpo_term'.", file=sys.stderr)
        sys.exit(0)
    
    if check_terms:
        for term in hpo_term:
            print(term)
            print(validate_term(term))
        sys.exit()
    
    hpo_list = []
    for term in hpo_term:
        if len(term.split(':')) < 2:
            term = ':'.join(['HP', term])
        hpo_list.append(term)
    
    results = query(hpo_list)
    for result in results:
        pp(result)

if __name__ == '__main__':
    try_query()

