# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db.models import Q

from django.template.defaultfilters import slugify
from website.apps.pronouns.tools import short_repr_row, full_repr_row

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        
        person = '3'
        number = 'pl'
        editor = orm['auth.User'].objects.all()[0]
        
        # 0. for each alignment
        for alignment in ["A", "S", "O", "P"]:
            
            # 1. get 3p plural g1 and g2
            qset = orm.PronounType.objects.filter(alignment=alignment, person=person, number=number)
            pt_3pplural_g1 = qset.filter(gender="M").get()
            pt_3pplural_g2 = qset.filter(gender="N").get()
            
            
            # 2. set gendered versions to late sequence
            seqid = pt_3pplural_g1.sequence
            pt_3pplural_g1.sequence = pt_3pplural_g1.sequence + 1000
            pt_3pplural_g1.save()
            print u"Resequenced %s" % pt_3pplural_g1
            pt_3pplural_g2.sequence = pt_3pplural_g2.sequence + 1000
            pt_3pplural_g2.save()
            print u"Resequenced %s" % pt_3pplural_g2
            
            
            p = {
                'alignment': alignment,
                'gender': None,
                'number': number,
                'person': person,
            }
            
            # 3. create a word
            word = orm['lexicon.Word'].objects.create(
                word=short_repr_row(p),
                full=full_repr_row(p),
                slug=slugify(short_repr_row(p)),
                editor=editor
            )
            print u"Created: %s, %s" % (word.word, word.slug)
            
            # 4. create new non-gendered version
            pt_combined = orm.PronounType.objects.create(
                alignment=alignment,
                person=person,
                number=number,
                gender=None,
                active=True,
                sequence=seqid,
                word=word,
                editor=editor
            )
            print u"Created: Combined Pronoun Type: %s" % unicode(pt_combined)
            
            # 4. go through each paradigm...
            for pdm in orm.Paradigm.objects.all():
                # 3a. add the new pronoun type
                pron = orm.Pronoun.objects.create(
                    paradigm=pdm,
                    pronountype=pt_combined,
                    editor=editor
                )
                print u"Created: Paradigm Pronoun: %s -> %s" % (pdm.language.slug, pron)
                
                # 3b. go through each pronoun/lexicon combination and copy them 
                items1 = orm.Pronoun.objects.filter(paradigm=pdm, pronountype=pt_3pplural_g1).get()
                items2 = orm.Pronoun.objects.filter(paradigm=pdm, pronountype=pt_3pplural_g2).get()
                items = list(items1.entries.all())
                items.extend([_ for _ in items2.entries.all()])
                seen = []
                for i in items:
                    if i.entry not in seen and i.entry not in (u'-', u'?', u''):
                        lex = orm['lexicon.Lexicon'].objects.create(
                            language = i.language,
                            source = i.source,
                            word = word,
                            entry = i.entry,
                            annotation = i.annotation,
                            editor=i.editor
                        )
                        pron.entries.add(lex)
                        print u"\tCreated: Lexicon: %s -> %s -> %s" % (pdm.id, pron, lex.entry)
                        seen.append(i.entry)
                
                pron.save()
            
            # 6. set gendered versions to inactive
            pt_3pplural_g1.active = False
            print u"Deactivated %s" % pt_3pplural_g1
            pt_3pplural_g2.active = False
            print u"Deactivated %s" % pt_3pplural_g2
            
            # 7. and save
            pt_3pplural_g1.save()
            pt_3pplural_g2.save()
            
            print("\n\n")
        
        
    def backwards(self, orm):
        "Write your backwards methods here."
        raise NotImplemented("Not Implemented!")
        
    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.alternatename': {
            'Meta': {'ordering': "['name']", 'object_name': 'AlternateName', 'db_table': "'altnames'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'core.attachment': {
            'Meta': {'object_name': 'Attachment', 'db_table': "'attachments'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': "'32'", 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"})
        },
        u'core.family': {
            'Meta': {'ordering': "['family']", 'object_name': 'Family', 'db_table': "'families'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'family': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'core.language': {
            'Meta': {'ordering': "['language', 'dialect']", 'unique_together': "(('isocode', 'language', 'dialect'),)", 'object_name': 'Language', 'db_table': "'languages'", 'index_together': "[['language', 'dialect']]"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'classification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dialect': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'family': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Family']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'isocode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'core.link': {
            'Meta': {'unique_together': "(['language', 'link'],)", 'object_name': 'Link', 'db_table': "'links'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'core.location': {
            'Meta': {'object_name': 'Location', 'db_table': "'locations'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.note': {
            'Meta': {'object_name': 'Note', 'db_table': "'notes'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"})
        },
        u'core.populationsize': {
            'Meta': {'object_name': 'PopulationSize', 'db_table': "'popsize'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'populationsize': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"})
        },
        u'core.source': {
            'Meta': {'ordering': "['author', 'year']", 'unique_together': "(['author', 'year'],)", 'object_name': 'Source', 'db_table': "'sources'", 'index_together': "[['author', 'year']]"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'bibtex': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'lexicon.cognate': {
            'Meta': {'object_name': 'Cognate', 'db_table': "'cognates'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cognateset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.CognateSet']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'flag': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexicon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.Lexicon']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']", 'null': 'True', 'blank': 'True'})
        },
        u'lexicon.cognateset': {
            'Meta': {'object_name': 'CognateSet', 'db_table': "'cognatesets'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexicon': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lexicon.Lexicon']", 'through': u"orm['lexicon.Cognate']", 'symmetrical': 'False'}),
            'protoform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']", 'null': 'True', 'blank': 'True'})
        },
        u'lexicon.correspondence': {
            'Meta': {'object_name': 'Correspondence', 'db_table': "'correspondences'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'corrset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.CorrespondenceSet']"}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'lexicon.correspondenceset': {
            'Meta': {'object_name': 'CorrespondenceSet', 'db_table': "'corrsets'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Language']", 'through': u"orm['lexicon.Correspondence']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']", 'null': 'True', 'blank': 'True'})
        },
        u'lexicon.lexicon': {
            'Meta': {'ordering': "['entry']", 'object_name': 'Lexicon', 'db_table': "'lexicon'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entry': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'loan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'loan_source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loan_source_set'", 'null': 'True', 'to': u"orm['core.Language']"}),
            'phon_entry': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.Word']"})
        },
        u'lexicon.word': {
            'Meta': {'ordering': "['word']", 'object_name': 'Word', 'db_table': "'words'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'full': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        u'lexicon.wordsubset': {
            'Meta': {'ordering': "['slug']", 'object_name': 'WordSubset', 'db_table': "'wordsubsets'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'}),
            'subset': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['lexicon.Word']", 'null': 'True', 'blank': 'True'})
        },
        u'pronouns.paradigm': {
            'Meta': {'object_name': 'Paradigm', 'db_table': "'paradigms'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'analect': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Source']"})
        },
        u'pronouns.pronoun': {
            'Meta': {'object_name': 'Pronoun', 'db_table': "'pronouns'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['lexicon.Lexicon']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paradigm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.Paradigm']"}),
            'pronountype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.PronounType']"})
        },
        u'pronouns.pronountype': {
            'Meta': {'object_name': 'PronounType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'alignment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.Word']"})
        },
        u'pronouns.relationship': {
            'Meta': {'object_name': 'Relationship', 'db_table': "'pronoun_relationships'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paradigm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.Paradigm']"}),
            'pronoun1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pronoun1'", 'to': u"orm['pronouns.Pronoun']"}),
            'pronoun2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pronoun2'", 'to': u"orm['pronouns.Pronoun']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'pronouns.rule': {
            'Meta': {'object_name': 'Rule', 'db_table': "'pronoun_rules'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paradigm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pronouns.Paradigm']"}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pronouns.Relationship']", 'null': 'True', 'blank': 'True'}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['core', 'lexicon', 'pronouns']
    symmetrical = True
