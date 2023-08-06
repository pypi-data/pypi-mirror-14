#!/usr/bin/env python 

import os, sys, getpass, traceback,json 
from collections import OrderedDict 
from dgitcore.helper import cd 
from dgitcore.plugins.transformer import TransformerBase
from dgitcore.config import get_config, ChoiceValidator, NonEmptyValidator 
import MySQLdb

class MySQLGenerator(TransformerBase):     
    """
    Simple generator backend for the datasets.

    Parameters
    ----------
    """
    def __init__(self): 
        self.enable = False 
        self.host = None
        self.port = 3036 
        self.username = None
        self.password = None
        super(MySQLGenerator, self).__init__('mysql-generator', 
                                             'v0', 
                                             "Materialize queries in dataset")
        
    def config(self, what='get', params=None): 
        
        if what == 'get': 
            return {
                'name': 'mysql-generator', 
                'nature': 'generator',
                'variables': ['enable', 'host', 'port', 'db', 'username', 'password'], 
                'defaults': { 
                    'enable': {
                        "value": 'y',
                        "description": "Enable content validation",
                        "validator": ChoiceValidator(['y','n'])
                    },
                    'host': {
                        "value": 'localhost',
                        "description": "MySQL server host name",
                        "validator": NonEmptyValidator()
                    },
                    'port': {
                        "value": '3306',
                        "description": "MySQL server port",
                        "validator": NonEmptyValidator()
                    },
                    'db': {
                        "value": '',
                        "description": "DB for MySQL access",
                        "validator": NonEmptyValidator()
                    },
                    'username': {
                        "value": getpass.getuser(),
                        "description": "Username for MySQL access",
                        "validator": NonEmptyValidator()
                    },
                    'password': {
                        "value": '',
                        "description": "Password for MySQL access",
                        "validator": NonEmptyValidator()
                    },
                }
            }
        else:
            if 'mysql-generator' not in params: 
                self.enable = 'n'
            else: 
                self.enable = params['mysql-generator']['enable'] 
                if self.enable == 'n': 
                    return 
                    
                # Collect parameters
                self.host = params['mysql-generator']['host']
                self.port = int(params['mysql-generator']['port'])
                self.db = params['mysql-generator']['db']
                self.username = params['mysql-generator']['username']
                self.password = params['mysql-generator']['password']
            
                # Test the connection 
                try: 
                    db=MySQLdb.connect(host=self.host,
                                       port=self.port, 
                                       db=self.db,
                                       user=self.username,
                                       passwd=self.password)
                    if db is None: 
                        print("Unable to connect to MySQL Server. Please check ini file") 
                        self.enable = 'n'
                    db.close() 

                except:
                    traceback.print_exc()
                    print("Unable to connect to MySQL Server. Please check ini file") 
                    self.enable = 'n'

    def autooptions(self): 
        return OrderedDict([
            ("files", ["*.sql"])
        ])

    def execute(self, cur, query): 
        """
        Execute a query...
        """

        # Execute
        rowcount = cur.execute(query)
        
        # Gather metadata 
        info = { 
            'rowcount': rowcount
        }

        # Get schema 
        mapping = MySQLdb.converters.conversions
        schema = []
        for field in cur.description: 
            name = field[0]
            ftype = mapping[field[1]][0]
            if isinstance(ftype, tuple): 
                ftype = "{} ({})".format(ftype[1].__name__, ftype[0])
            schema.append({'name': name, 'type': ftype})

        # Get content
        content = ""
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        content += "\t".join(field_names)
        first = True
        for row in cur.fetchall():
            if first: 
                for i,v in enumerate(row):
                    schema[i]['sample'] = str(v)
                first = False 
            content += "\n" + "\t".join(list(row))

        schema = json.dumps(schema, indent=4)
        info = json.dumps(info, indent=4)
        return (info, schema, content) 

    def  evaluate(self, repo, spec, force=False): 
        """
        Evaluate an SQL query, cache the results in server
        """
        
        files = spec.get('files', [])

        if len(files) == 0: 
            # Nothing to do 
            return [] 

        db=MySQLdb.connect(host=self.host,
                           port=self.port, 
                           db=self.db,
                           user=self.username,
                           passwd=self.password)
        cur = db.cursor()

        result = []
        with cd(repo.rootdir): 
            for f in files: 
                
                cachepath = repo.cache_path(self.name, f + '.data')                
                if not force and repo.cache_check(cachepath):
                    #print("Found in cache")
                    result.append({
                        'target': f,
                        'transformer': self.name,
                        'status': 'OK',
                        'message': 'Result already cached ({})'.format(cachepath['relative'])
                    })
                    continue

                # print("Not found in cache. So executing")
                # Run the query 
                query = open(f).read()
                (info, schema, content) = self.execute(cur, query) 

                # Save the results 
                for output in [['info', info], ['schema', schema], ['data', data]]:
                    cachepath = repo.cache_path(self.name, f + "." + output[0])
                    repo.cache_write(cachepath, output[1]) 

                result.append({
                    'target': files[0],
                    'transformer': self.name,
                    'status': 'OK',
                    'message': 'Executed the query'
                })
                
        return result 

def setup(mgr): 

    obj = MySQLGenerator() 
    mgr.register('transformer', obj)

