#!/usr/bin/env python

import json
import logging
import urllib2


 
def load_json(source):
    """
    get the json data either from URL or from file
    """
    #log.debug('Starting with source %s' %source)
    if source.startswith('http'):
        data = json.load(urllib2.urlopen(source))
    else:
        data = json.load(open(source))
    #log.debug('Leaving with output %s.' %data)
    return data

