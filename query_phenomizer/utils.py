#!/usr/bin/env python
# encoding: utf-8
"""
query.py

query phenomizer and store the results in a ordered dictionary.

Created by Måns Magnusson on 2015-02-02.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""
from __future__ import print_function

import logging
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
                'gene_symbols': list(str),
                'disease_nr': int,
                'disease_source': str,
                'description': str,
                'raw_line': str
             }
             
    """
    
    if line.startswith("Problem"):
        raise RuntimeError("Login credentials seems to be wrong")

    result = {
        'p_value': None,
        'gene_symbols': [],
        'disease_nr': None,
        'disease_source': None,
        'description': None,
        'raw_line': line
    }
    
    result['raw_line'] = line.rstrip()
    result_line = line.rstrip().split('\t')
    
    try:
        result['p_value'] = float(result_line[0])
    except ValueError:
        pass

    try:
        medical_litterature = result_line[2].split(':')
        result['disease_source'] = medical_litterature[0]
        result['disease_nr'] = int(medical_litterature[1])
    except IndexError:
        pass

    try:
        description = result_line[3]
        result['description'] = description
    except IndexError:
        pass

    if len(result_line) > 4:
        for gene_symbol in result_line[4].split(','):
            result['gene_symbols'].append(gene_symbol.strip())

    return result

def query_phenomizer(usr, pwd,  *hpo_terms):
    """
    Query the phenomizer web tool
    
    Arguments:
        usr (str): A username for phenomizer
        pwd (str): A password for phenomizer
        hpo_terms (list): A list with hpo terms
    
    Returns:
        raw_answer : The raw result from phenomizer
    """
    base_string = 'http://compbio.charite.de/phenomizer/phenomizer/PhenomizerServiceURI'
    questions = {'mobilequery':'true', 'terms':','.join(hpo_terms), 'username':usr, 'password':pwd}
    try:
        r = requests.get(base_string, params=questions, timeout=10)
    except requests.exceptions.Timeout:
        raise RuntimeError("The request timed out.")
        
    if not r.status_code == requests.codes.ok:
        raise RuntimeError("Phenomizer returned a bad status code: %s" % r.status_code)
    
    r.encoding = 'utf-8'
    
    return r

def query(usr, pwd, *hpo_terms):
    """
    Query the phenomizer web tool
    
    Arguments:
        usr (str): A username for phenomizer
        pwd (str): A password for phenomizer
        hpo_terms (list): A list with hpo terms
    
    yields:
        parsed_term (dict): A dictionary with the parsed information
                            from phenomizer
     
    """
    raw_result = query_phenomizer(usr, pwd, *hpo_terms)
    
    for line in raw_result.text.split('\n'):
        if len(line) > 1:
            if not line.startswith('#'):
                yield parse_result(line)
    

def validate_term(usr, pwd, hpo_term):
    """
    Validate if the HPO term exists.
    
    Check if there are any result when querying phenomizer.
    
    Arguments:
        usr (str): A username for phenomizer
        pwd (str): A password for phenomizer
       hpo_term (string): Represents the hpo term
    
    Returns:
        result (boolean): True if term exists, False otherwise
    
    """
    
    result = True
    try:
        for line in query(usr, pwd, hpo_term):
            pass
    except RuntimeError as err:
        raise err
    
    return result
    
