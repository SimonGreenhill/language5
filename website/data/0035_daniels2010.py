#!/usr/bin/env python
#coding=utf-8

import os
import codecs
from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon, Cognate, CognateSet


REFERENCE = "Daniels, D. 2010. A preliminary phonological history of the Sogeram languages of Papua New Guinea. Oceanic Linguistics, 49, 163-193."

DATAFILE = os.environ['IMPORTER_FILENAME'].replace('.py', '.dat')

LANGUAGES = {
    'Atemple': Language.objects.get(slug="atemble"),
    'Nend': Language.objects.get(slug="nend"),
    'Apali': Language.objects.get(slug="apali"),
    'Manat': Language.objects.get(slug="manat"),
    
    'Mum': Language.objects.get(slug="mum"),
    'Sirva': Language.objects.get(slug="sirva"),
    
    'Aisi': Language.objects.get(slug="aisi"),
    'Kulsab': Language.objects.get(slug="kulsab"),
    
    '*Sogeram': Language.objects.get(slug="proto-sogeram"),
    '*W Sogeram': Language.objects.get(slug="proto-western-sogeram"),
    '*E Sogeram': Language.objects.get(slug="proto-eastern-sogeram"),
    '*C Sogeram': Language.objects.get(slug="proto-central-sogeram"),    
}


# get editor
Ed = User.objects.get(pk=1)

SObj = Source.objects.create(year=2010, author="Daniels", slug="daniels2010",
                          reference=REFERENCE, bibtex="", comment="",
                          editor=Ed)

cognates = {}
_created = 0
with codecs.open(DATAFILE, 'rU', encoding="utf8") as handle:
    for line in handle.readlines():
        wslug, lang, entry, cogid, comment = [_.strip() for _ in line.split("\t")]
        # find WObj
        WObj = Word.objects.get(slug=wslug)
        
        # find LObj
        LObj = LANGUAGES.get(lang)
        assert LObj is not None
        
        # process comment
        is_loan, loan_source = False, None
        comment = comment.strip()
        if comment is not u"":
            if comment.startswith("LOAN:"):
                is_loan = True
                loan_source = LANGUAGES.get(comment.split(":")[1])
                assert loan_source is not None
            elif '(C)' in comment:
                comment = comment.replace("(C)", u"(Acɨ dialect)").strip()
        
        # create lexicon
        lex = Lexicon.objects.create(
            language=LObj, 
            source=SObj,
            word=WObj, 
            entry=entry, 
            annotation=comment, 
            editor=Ed
        )
        lex.save()
        _created += 1
        print(u"Created Lexicon: {}".format(lex))
        # handle is_loan == True and loan_source
        
        # store with cogset.
        cognates[cogid] = cognates.get(cogid, [])
        cognates[cogid].append(lex)
        

# and create cognate sets..
for cogid in cognates:
    members = cognates[cogid]
    # find proto-sogeram
    psog = None
    for lex in members:
        if lex.language.slug == 'proto-sogeram':
            psog = lex
    assert psog is not None, "Can't find Proto-Sogeram form!"
    
    CogSet = CognateSet.objects.create(
        protoform=psog.entry,
        gloss=psog.word.word,
        source=SObj,
        comment="MR-{}".format(cogid),
        quality='1', # published
        editor=Ed
    )
    CogSet.save()
    _created += 1
    print(u"Created Cogset: {} ({})".format(CogSet.id, CogSet.comment))
    for lex in members:
        cog = Cognate.objects.create(lexicon=lex, cognateset=CogSet, source=SObj, editor=Ed)
        cog.save()
        _created += 1
        print(u"\t Added Cognate: {} -> {}".format(lex, CogSet.id))
    
print("---- TOTAL {} ----".format(_created))