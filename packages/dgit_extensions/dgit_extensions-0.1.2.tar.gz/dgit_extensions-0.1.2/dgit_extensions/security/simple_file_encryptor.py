#!/usr/bin/env python 

import os, sys, getpass, traceback, json 
import csv
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import copy 
from hashlib import sha256 
from collections import OrderedDict 
from dgitcore.helper import cd, run 
from dgitcore.plugins.transformer import TransformerBase
from dgitcore.config import get_config, ChoiceValidator, NonEmptyValidator 
from dgitcore.exceptions import * 

class SimpleFileEncryptor(TransformerBase):     
    """
    Encrypt specified files using openssl
    """
    def __init__(self): 
        self.enable = 'y'
        super(SimpleFileEncryptor, self).__init__('simple-file-encryptor', 
                                              'v0', 
                                              "Simple encryptor of files")
        
    def config(self, what='get', params=None): 
        
        if what == 'get': 
            return {
                'name': 'simple-file-encryptor',
                'nature': 'transformer',
                'variables': []
            }
        else: 
            return 


    def autooptions(self): 
        return OrderedDict([
            ("files", ["*.tsv", "*.csv"]),
        ])

    def  evaluate(self, repo, spec, force, args): 
        """
        Evaluate an SQL query, cache the results in server
        """
        
        files = spec['files'] 

        result = []
        encryption_suite = key = None 
        
        for f in files: 

            r = repo.get_resource(f) 

            # Check if we have already computed it...
            cachepath = repo.cache_path(self.name, f, ext='encrypted')
            if not force and repo.cache_check(cachepath): 
                result.append({
                    'target': f,
                    'transformer': self.name,
                    'status': 'OK',
                    'message': 'Result already cached ({})'.format(cachepath['relative'])
                })
                continue 

            inputfile = r['localfullpath']
            outputfile = cachepath['full'] 

            try: 
                os.makedirs(os.path.dirname(outputfile))
            except:
                pass 

            # Run openssl encryptor
            cmd = ['openssl', 'aes-256-cbc', '-salt', '-in', inputfile, '-out', outputfile]
            run(cmd)

            # Add the result
            result.append({
                'target': f,
                'transformer': self.name,
                'status': 'OK',
                'message': 'Result already cached ({})'.format(cachepath['relative']) + \
                          '. Decrypt using "openssl aes-256-cbc -salt -d -in ... -out ..."'
            })

        return result 

def setup(mgr): 

    obj = SimpleFileEncryptor()
    mgr.register('transformer', obj)

