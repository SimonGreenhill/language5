#!/usr/bin/env python
import os
import gzip
import json

from django.contrib.auth.models import User
from website.apps.lexicon.models import Lexicon, Word
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun

def get_field(content, var):
    if var in content[u'fields']:
        return content[u'fields'].get(var)
    else:
        raise ValueError("{0} not in content".format(var))

def handle_pronoun(content):
    pk = int(content.get(u'pk'))
    comment = get_field(content, u'comment')
    added = get_field(content, u'added')
    form = get_field(content, u'form')
    editor_id = int(get_field(content, u'editor'))
    paradigm_id = int(get_field(content, u'paradigm'))
    # get paradigm
    pdm = Paradigm.objects.get(pk=paradigm_id)
    
    ptype = PronounType.objects.get(
        alignment=get_field(content, u'alignment'),
        number=get_field(content, u'number'),
        gender=get_field(content, u'gender'),
        person=get_field(content, u'person')
    )
    
    # have we got a pronoun...?
    pron = Pronoun.objects.filter(
        paradigm_id=paradigm_id,
        pronountype=ptype
    )[0]
    assert pron, "Pronoun not found: {0}".format(ptype)
    
    if get_field(content, u'comment') is not None and len(get_field(content, u'comment')) > 0:
        pron.comment = get_field(content, u'comment')
        
    for f in form.split(","):
        f = f.strip()
        if len(f) > 0:
            lex = Lexicon.objects.create(
                entry=f,
                language_id=pdm.language.id,
                source_id=pdm.source.id,
                word=ptype.word,
                editor_id=editor_id
            )
            lex.save()
            print("Created Lexicon: {0} - {1} - {2} {3}".format(
                pdm.language, ptype, lex, 
                '(%s)' % pron.comment if pron.comment is not None else '')
            )
            
            # 5. add to entries for this Pronoun.
            pron.entries.add(lex)
    
    pron.save()


def handle_paradigm(content):
    p = Paradigm.objects.create(
        pk=content.get(u'pk'),
        editor_id = get_field(content, u'editor'),
        source_id = get_field(content, u'source'),
        added = get_field(content, u'added'),
        language_id = get_field(content, u'language'),
        comment = get_field(content, u'comment')
    )
    p.save()
    p._prefill_pronouns()
    print("Created Paradigm: {0}".format(p))


def null_handler(content): 
    pass


handlers = {
    'pronouns.pronoun': handle_pronoun,
    'pronouns.paradigm': handle_paradigm,
    'pronouns.rule': null_handler,
    'pronouns.relationship': null_handler,
}


filename = os.path.join(
     os.environ['IMPORTER_DATAROOT'],
    "0007_pronouns_old_data.json.gz"
)

assert os.path.isfile(filename), "Filename {0} is not found".format(filename)

with gzip.open(filename, 'rb') as handle:
    data = json.loads(handle.read())
    
ed = User.objects.get(pk=1) # get editor

for entity in data:
    fun = handlers.get(entity[u'model'])
    if fun is None:
        pass#print "Unhandled Entity: {0}".format(entity[u'model'])
    else:
        print entity[u'model'], entity[u'pk']
        objs = fun(entity)

