#!/usr/bin/env python
# encoding: utf-8
"""
query_phenomizer

Command line script for query phenomizer database.

Created by Måns Magnusson on 2015-02-02.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""
from __future__ import print_function

import logging
import click
import json

from query_phenomizer import query, validate_term

from .log import (configure_stream, LEVELS)

logger = logging.getLogger(__name__)

def test_args(*args):
    """docstring for test_args"""
    for arg in args:
        print(arg)

@click.command()
@click.argument('hpo_term',
        nargs=-1,
)
@click.option('-u', '--username',
        type=str,
        help="A username for phenomizer"
)
@click.option('-p', '--password',
        type=str,
        help="A password for phenomizer"
)
@click.option('-c', '--check_terms',
        is_flag=True,
        help="Check if the term(s) exist"
)
@click.option('-o', '--output',
        type=click.File('wb'),
        help="Specify the path to a file for storing the phenomizer output."
)
@click.option('--p_value_limit',
        default=1.0,
        show_default=True,
        help='Specify the highest p-value that you want included.'
)
@click.option("--to-json",
        is_flag=True,
        help="If result should be printed to json format"
)
@click.option('-v', '--verbose',
        count=True,
        default=2
)
@click.pass_context
def cli(ctx, hpo_term, check_terms, output, p_value_limit, verbose, username, 
        password, to_json):
    "Give hpo terms either on the form 'HP:0001623', or '0001623'"    
    loglevel = LEVELS.get(min(verbose, 3))
    configure_stream(level=loglevel)
    
    if not hpo_term:
        logger.info("Please specify at least one hpo term with '-t/--hpo_term'.")
        ctx.abort()

    if not (username and password):
        logger.info("Please a username and a password.")
        logger.info("Contact sebastian.koehler@charite.de.")
        ctx.abort()
    
    hpo_list = []
    for term in hpo_term:
        if len(term.split(':')) < 2:
            term = ':'.join(['HP', term])
        hpo_list.append(term)
    
    logger.info("HPO terms used: {0}".format(','.join(hpo_list)))
    
    if check_terms:
        for term in hpo_list:
            if not validate_term(username, password, term):
                logger.info("HPO term : {0} does not exist".format(term))
            else:
                logger.info("HPO term : {0} does exist!".format(term))
        ctx.abort()
    else:
        click.echo("{0}\t{1}\t{2}\t{3}".format(
            'p_value', 'disease', 'description', 'genes'
        ))
        try:
            for result in query(username, password, *hpo_list):
                if to_json:
                    click.echo(json.dumps(result))
                else:
                    click.echo("{0}\t{1}:{2}\t{3}\t{4}".format(
                        result['p_value'], 
                        result['disease_source'],
                        result['disease_nr'],
                        result['description'],
                        ','.join(result['gene_symbols'])
                    ))
                
        except RuntimeError as e:
            logger.error(e.message)
            ctx.abort()
        
        # nr_significant_genes = 0
        # for result in results:
        #     if result['p_value'] < p_value_limit:
        #         nr_significant_genes += 1
        #         if output:
        #             output.write(result['raw_line'] + '\n')
        #         else:
        #             print(json.dumps(result))
        #
        # if nr_significant_genes == 0:
        #     logger.info("There where no significant genes with p value"\
        #                 " < {0}".format(p_value_limit))

