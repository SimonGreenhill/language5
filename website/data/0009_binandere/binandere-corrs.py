#!/usr/bin/env python
#coding=utf-8
"""..."""
__author__ = 'Simon Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2012 Simon Greenhill'
__license__ = 'New-style BSD'
import codecs
import pdftables

badchars = {
    '(cid:1317)': u'ə',
    '(cid:1860)': u'ɲ',
    '(cid:1845)': u'ɣ',
    '(cid:2555)': u'Ṽ',
    '(cid:446)': u'ŋ',
    '(cid:1866)': u'ɸ',
    '(cid:1146)': u'̃',
    '(cid:537)': u'\xd8',
    
}

def clean(var):
    #var = var.encode('utf8')
    var = var.strip()
    for b in badchars:
        var = var.replace(b, badchars[b])
    return var
    
    



if __name__ == '__main__':
    
    languages = {}
    
    with open('binandere-corrs.pdf', 'rb') as fh:
        for i in range(1,5):
            print i
            page = pdftables.get_pdf_page(fh, i)
            page, diagnosticData = pdftables.page_to_tables(page, 
                                                extend_y = False, 
                                                atomise = False)
            for row in page:
                row = [clean(_) for _ in row]
                language = row.pop(0)
                
                languages[language] = languages.get(language, {})
                
                for j, corr in enumerate(row, 1):
                    corr_index = "%d-%d" % (i,j )
                    print language, corr_index, corr
                    assert corr_index not in languages[language]
                    languages[language][corr_index] = corr
            
    import json
    with codecs.open('0010-binandere-corrs.json', 'w', encoding="utf8") as handle:
        handle.write(json.dumps(languages, indent=2))
