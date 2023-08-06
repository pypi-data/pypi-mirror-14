#!/usr/bin/env python 

import os, sys, getpass, traceback,json 
import csv
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import copy 
from hashlib import sha256 
from collections import OrderedDict 
from dgitcore.helper import cd 
from dgitcore.plugins.transformer import TransformerBase
from dgitcore.config import get_config, ChoiceValidator, NonEmptyValidator 
from dgitcore.exceptions import * 

class SimpleTableAnonymizer(TransformerBase):     
    """
    Simple anonymizer for datasets

    Supported transforms: 
    
    1. Hash: Replace a field by sha256 hash 
    2. Randomize: Replace a numeric field by a random number 

    Parameters
    ----------
    """
    def __init__(self): 
        self.enable = 'y'
        super(SimpleTableAnonymizer, self).__init__('simple-table-anonymizer', 
                                              'v0', 
                                              "Simple anonymizer for tables")
        
    def config(self, what='get', params=None): 
        
        if what == 'get': 
            return {
                'name': 'simple-table-anonymizer',
                'nature': 'transformer',
                'variables': []
            }
        else: 
            return 


    def autooptions(self): 
        return OrderedDict([
            ("files", ["*.tsv", "*.csv"]),
            ("rules", OrderedDict([
                ("hash", ["Name", "Email Id"]),
                ("randomize", ["Mobile Number"])
            ])),
            ("rules-files", [])
        ])

    def merge(self, rules, rules_files): 
        """
        When rules are specifed in options file or in the rules file,
        load them.
        """
        final = {} 
        if rules is not None: 
            final = rules 
            
        if rules_files is None: 
            return final 

        # Incorporate rules from all the files
        for f in rules_files:             
            update = json.loads(open(f).read())
            final.update(update) 
            
        return final 

    def apply_rules_row(self, row, rules): 
        """
        Apply rules to one row 
        """
        row = copy.copy(row) 
        for rulename in rules: 
            if rulename == "hash":
                columns = rules[rulename] 
                for c in columns: 
                    if c in row: 
                        h = sha256()
                        h.update(row[c].encode('utf-8'))
                        row[c] = h.hexdigest() 
        
        return row 

    def apply_rules_file(self, repo, f, rules): 
        """
        Apply all the rules to one file
        """
        
        # Where can I find this source in my filesystem? 
        r = repo.get_resource(f)
        
        # Can I even handle the file? 
        ext = f.lower().split(".")[-1]
        if ext not in ['csv','tsv']: 
            return None 
            
        # get the delimited 
        delimiter=","
        if f.lower().split(".")[-1] == 'tsv': 
            delimiter="\t"

        transformed = [] 
        fieldnames = None
        with open(r['localfullpath']) as fd: 
            try:
                reader = csv.DictReader(fd, delimiter=delimiter)
                fieldnames = reader.fieldnames
                for row in reader:
                    newrow = self.apply_rules_row(row, rules) 
                    transformed.append(newrow) 
            except: 
                raise InvalidFileContent(f)


        # Write the content to a buffer..
        content = StringIO()
        writer = csv.DictWriter(content, 
                                delimiter=delimiter, 
                                fieldnames=fieldnames) 
        writer.writeheader()
        for row in transformed: 
            writer.writerow(row) 

        return content.getvalue().strip('\r\n')

    def  evaluate(self, repo, spec, force, args): 
        """
        Evaluate an SQL query, cache the results in server
        """
        
        files = spec['files'] 
        rules = spec.get('rules', None)
        rules_files = spec.get('rules-files', None) 

        # Sanity check 
        if rules is None and rules_files is None: 
            raise IncompleteParameters("Either rules or rules_files have to be specified") 
            
        # Get final version of the rules 
        rules = self.merge(rules, rules_files) 

        result = []

        for f in files: 

            # Get extension 
            ext = f.lower().split(".")[-1]

            # Check if we have already computed it...
            cachepath = repo.cache_path(self.name, f + '.data', ext=ext)
            if not force and repo.cache_check(cachepath): 
                result.append({
                    'target': f,
                    'transformer': self.name,
                    'status': 'OK',
                    'message': 'Result already cached ({})'.format(cachepath['relative'])
                })
                continue 

            # Now apply the rules 
            content = self.apply_rules_file(repo, f, rules) 
            repo.cache_write(cachepath, content) 

            # Add the result
            result.append({
                'target': f,
                'transformer': self.name,
                'status': 'OK',
                'message': 'Result already cached ({})'.format(cachepath['relative'])
            })

        return result 

def setup(mgr): 

    obj = SimpleTableAnonymizer()
    mgr.register('transformer', obj)

