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

from os import linesep
from query_phenomizer import query, validate_term

from getpass import getpass

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
@click.option('-c', '--check-terms',
        is_flag=True,
        help="Check if the term(s) exist"
)
@click.option('-o', '--output',
        type=click.File('wb'),
        help="Specify the path to a file for storing the phenomizer output."
)
@click.option('--p-value-limit',
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
    """Give hpo terms either on the form 'HP:0001623', or '0001623'.

    If -p is not used, a password prompt will appear instead."""
    loglevel = LEVELS.get(min(verbose, 3))
    configure_stream(level=loglevel)
    
    if not hpo_term:
        logger.info("Please specify at least one hpo term with '-t/--hpo_term'.")
        ctx.abort()

    if not username:
        logger.info("Please specify username with -u (and password with -p).")
        logger.info("Contact sebastian.koehler@charite.de.")
        ctx.abort()

    if not password:
        password = getpass("password:")
    
    hpo_list = []
    for term in hpo_term:
        if len(term.split(':')) < 2:
            term = ':'.join(['HP', term])
        hpo_list.append(term)
    
    logger.info("HPO terms used: {0}".format(','.join(hpo_list)))
    
    if check_terms:
        for term in hpo_list:
            try:
                if not validate_term(username, password, term):
                    logger.info("HPO term : {0} does not exist".format(term))
                else:
                    logger.info("HPO term : {0} does exist!".format(term))
            except RuntimeError as err:
                click.echo(err)
                ctx.abort()
        ctx.abort()
    else:
        try:
            if output:
                header = "p-value\tdisease-id\tdisease-name\tgene-symbols" + linesep  # The file header.
                output.write(header.encode())  # "a bytes-like object is required"
            for result in query(username, password, *hpo_list):
                if to_json:
                    click.echo(json.dumps(result))
                else:
                    print_string = "{0}\t{1}:{2}\t{3}\t{4}".format(
                        result['p_value'],
                        result['disease_source'],
                        result['disease_nr'],
                        result['description'],
                        ','.join(result['gene_symbols'])
                    )
                    p_value = result['p_value']
                    if p_value <= p_value_limit:
                        if output:
                            print_string += linesep  # Adds line separator to output.
                            output.write(print_string.encode())  # "a bytes-like object is required"
                        else:
                            click.echo(print_string)
                
        except RuntimeError as e:
            click.echo(e)
            ctx.abort()
        finally:
            if output:
                output.flush()
                output.close()
