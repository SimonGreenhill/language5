#!/usr/bin/env python

import MySQLdb
import getpass
import sys
import os
from datetime import datetime

from django.template.defaultfilters import slugify


HOST='localhost'
DB='austronesian'
USER='root'

LIMIT = None #20
LIMIT = 20

DATABASE_LIST = ['austronesian', 'bantu', 'mayan', 'utoaztecan']


def get_families(database):
    """Returns a list of unique families in the given database"""
    F = []
    cursor.execute(
        "SELECT DISTINCT LEFT(classification, LOCATE(',', classification)-1) FROM %s.languages" % database
    )
    for row in cursor.fetchall():
        if len(row[0]) > 0:
            F.append(row[0])
    return F

def get_languages(database, LIMIT=None):
    """Returns a dictionary of languages from the given database"""
    languages = {}
    keylist = ['id', 'language', 'author', 'notes', 'problems', 'silcode', 'classification', 'typedby']
    q = "SELECT %s FROM %s.languages ORDER BY id" % (", ".join(keylist), database)
    if LIMIT is not None:
        q += ' LIMIT %d' % LIMIT
    cursor.execute(q)
    for row in cursor.fetchall():
        id = row[0]
        languages[id] = {}
        for i, k in enumerate(keylist):
            value = row[i]
            if value is None:
                value = ''
            if k == 'silcode':
                k = 'isocode'
            elif k == 'classification':
                languages[id]['family'] = value.split(',')[0]
            elif k == 'language':
                languages[id]['slug'] = slugify(value)
                k = 'name'
            languages[id][k] = value
    return languages

def get_resources(database, language_id):
    """Returns a dict. of all the resources for a given database/language_id"""
    cursor.execute(
        "SELECT link, description FROM %s.resources WHERE language_id=%d" % (database, language_id)
    )
    res = []
    for lnk, desc in cursor.fetchall():
        res.append((lnk, desc))
    return res

def get_locations(database, language_id):
    """Returns a list of all the locations in the database for a given language_id"""
    locs = []
    cursor.execute(
        "SELECT longitude, latitude FROM %s.locations WHERE language_id=%d" % (database, language_id)
    )
    for lon, lat in cursor.fetchall():
        locs.append((lon, lat))
    return locs


if __name__ == '__main__':
    print "Importing LPAN data..."
    DUMMYRUN = False
    if len(sys.argv) > 1 and sys.argv[1] == 'dummy':
        DUMMYRUN = True
        print "WARNING: Dummy run - no data will be saved!"
    
    # finalise imports
    from bin import bootstrap
    bootstrap()
    
    from django.conf import settings
    from languages.models import Language, AlternateNames, Family, Links, Locations
    
    from django.contrib.auth.models import User
    ed = User.objects.get(pk=1)
    
    # get database password
    #passwd = getpass.getpass()
    passwd = 'g17acr04'
    
    # init connection
    connection = MySQLdb.connect(host=HOST, user=USER, passwd=passwd, db=DB)
    cursor = connection.cursor()
    
    # STEP 1:
    print "Extracting Families..."
    families = {}
    for database in DATABASE_LIST:
        for f in get_families(database):
            if f not in families.keys():
                fam = Family(name=f, slug=slugify(f), editor=ed, added=datetime.now())
                print "\t", fam
                families[slugify(f)] = fam
                if DUMMYRUN == False:
                    fam.save()
    
    print
    print "Extracting Languages..."
    languages = {}
    default_sources = {}
    for database in DATABASE_LIST:
        languages[database] = {}
        default_sources[database] = {}
        block = get_languages(database, LIMIT)
        for language_id, data in block.iteritems():
            languages[database][language_id] = data.copy()
            
            print "\tInstalling %s/%d: %s..." % (database, language_id, data['slug'])
            data['editor'] = ed
            data['added'] = datetime.now()
            # ignore language_id's from databases OTHER than Austronesian,
            # the ABVD id's have been cited, and should be therefore retained, whilst
            # the other id codes haven't.
            if database != u'austronesian':
                del(data['id'])
            
            # add to family
            try:
                f = families.get(slugify(data['family']))
            except KeyError:
                raise "Unknown family '%s'" % slugify[data['family']]
            print '\t\tadding to "%s" family.' % f.slug
            data['family'] = f
            
            # save..
            l = Language()
            for k, v in data.iteritems():
                setattr(l, k, v)
            if DUMMYRUN == False:
                l.save()
            
            
            # do resources
            for lnk, des in get_resources(database, language_id):
                print '\t\tinstalling resource %s' % lnk[0:40]
                if DUMMYRUN == False:
                    Links.objects.create(language=l, link=lnk, description=des, editor=ed, added=datetime.now())
            
            # do locations
            #print ' WARNING: locations not installed'
            for lg, lt in get_locations(database, language_id):
                print '\t\tinstalling location %3.4f:%3.4f' % (lg, lt)
                if DUMMYRUN == False:
                    Locations.objects.create(language=l, longitude=lg, latitude=lt, editor=ed, added=datetime.now())
            
            print '\t\tTODO: Author', data['author'][0:60]
            print '\t\tTODO: Notes', data['notes'][0:60]
            print '\t\tTODO: Problems', data['problems'][0:60]
            print '\t\tTODO: Typedby', data['typedby'][0:60]
            
            
            ###default_sources[database][language_id] = guess_default_source(data['author'], data['notes'], data['problems'])
        
    raise Exception, "Not Implemented from here.. "
    print 'Extracting Words....'
    print '  TODO: Words', '...'
    print '  TODO: Word Categories', '...'
    print '  TODO: Word Categories Members', '...'
    
    print 'Extracting Data...'
    print '  TODO: History', '...'
    print '  TODO: Data', '...'
    
    print 'Extracting Statistics...'
    
    print '  TODO: statistics'
    print '  TODO: lang_popularity'
    print '  TODO: word_popularity'
    
    print 'Extracting Comments...'
    print '  TODO: comments'
    
    print "TODO::: WHATEVER'S IN GENERAL?!"
    
