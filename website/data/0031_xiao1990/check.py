#!/usr/bin/env python
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2014 Simon J. Greenhill'
__license__ = 'New-style BSD'

import requests


if __name__ == '__main__':
    
    url = "http://transnewguinea.org/api/v1/word/?format=json&limit=1000"
    
    r = requests.get(url)
    words = []
    for obj in r.json()['objects']:
        words.append(obj['slug'])
    
    with open('Xiao.txt', 'rU') as handle:
        for line in handle.readlines():
            line = line.strip().split(" ")[0]
            if line not in words:
                print line




