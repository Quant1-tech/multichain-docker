# et *- coding: utf-8 -*-
"""
Created on Wed Jun 14 09:52:13 2017
by eduardo perez (edunuke at github)
"""

import os
import requests
import json
import logging
from subprocess import Popen

log = logging.getLogger(__name__)
#%%
class api_call():
    
    __id_count = 0
    
    def __init__(self, rpcuser, rpcpasswd, 
                 rpchost, rpcport, chainname, rpc_call= None):
        self.__rpcuser = rpcuser
        self.__rpcpasswd = rpcpasswd
        self.__rpchost = rpchost
        self.__rpcport = rpcport
        self.__chainname = chainname
        self.__auth_header = ':'.join([rpcuser, rpcpasswd])
        self.__headers = {'Host': self.__rpchost,
                          'User-Agent': 'multichainrpc',
                          'Authorization': self.__auth_header,
                          'Content-type': 'application/json'
                          }
        self.__rpc_call = rpc_call

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError
        if self.__rpc_call is not None:
            name = "%s.%s" % (self.__rpc_call, name)
        return api_call(self.__rpcuser,
                          self.__rpcpasswd,
                          self.__rpchost,
                          self.__rpcport,
                          self.__chainname,
                          name)
    def __call__(self, *args):
        api_call.__id_count += 1
        postdata = {'chain_name': self.__chainname,
                    'version':"1.0.0.dev",
                    'params': args,
                    'method': self.__rpc_call,
                    'id': api_call.__id_count}
        url = "http://%s:%s@%s:%s"%(self.__rpcuser,self.__rpcpasswd, 
                                    self.__rpchost, self.__rpcport)
        encoded = json.dumps(postdata)
        log.debug("Request: %s" % encoded)
        r = requests.post(url, data=encoded, headers=self.__headers)
        if r.status_code == 200:
            log.debug("Response: %s" % r.json())
            return r.json()['result']
        else:
            log.error("Error! Status code: %s" % r.status_code)
            log.debug("Text: %s" % r.text)
            return r.json()

