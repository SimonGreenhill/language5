# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from website.apps.pronouns.tools import short_repr_row, full_repr_row


PronounCombinations = [
    # 1st (excl) Person, Sing.
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('1', '1st (excl) Person')
    },
    # 1st (excl) Person, Dual.
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('1', '1st (excl) Person')
    },
    
    # 1st (excl) Person, Plural
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('1', '1st (excl) Person')
    },
    
    # 1st (incl) Person, Dual
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('12', '1st (incl) Person')
    },
    
    # 1st (incl) Person, Plural
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('12', '1st (incl) Person')
    },
    
    # 2nd person Sg.
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('sg', 'Singular'),
        'person': ('2', '2nd Person')
    },
    # 2nd Person Dual. 
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('du', 'Dual'),
        'person': ('2', '2nd Person')
    },
    # 2nd Person, Plural
    {
        'alignment': ('A', 'A'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': None,
        'number': ('pl', 'Plural'),
        'person': ('2', '2nd Person')
    },
    # 3rd Person ----- INCLUDES GENDER
    {
        'alignment': ('A', 'A'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('M', 'Masculine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('F', 'Feminine'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {   
        'alignment': ('A', 'A'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('N', 'Neuter'),
        'number': ('sg', 'Singular'),
        'person': ('3', '3rd Person')},
    {
        'alignment': ('A', 'A'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('M', 'Masculine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('F', 'Feminine'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('N', 'Neuter'),
        'number': ('du', 'Dual'),
        'person': ('3', '3rd Person')},
    {
        'alignment': ('A', 'A'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('M', 'Masculine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('F', 'Feminine'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('A', 'A'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('S', 'S'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('O', 'O'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    },
    {
        'alignment': ('P', 'Possessive'),
        'gender': ('N', 'Neuter'),
        'number': ('pl', 'Plural'),
        'person': ('3', '3rd Person')
    }
]

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        editor = orm['auth.User'].objects.all()[0]
        
        words = {}
        # create words
        for p in PronounCombinations:
            # create word
            w = short_repr_row(p)
            f = full_repr_row(p)
            slug = w.lower().replace(" ", "_")
            print u"%s -> %s: %s" % (slug, w, f)
            
            word = orm['lexicon.Word'].objects.create(
                word = w,
                slug = slug,
                full = f,
                editor=editor
            )
            word.save()
            
            words[w] = word
                 
            if p['gender'] is None:
                gender = None
            else:
                gender = p['gender'][0]
            
            ptype = orm['pronouns.pronountype'].objects.create(
                alignment = p['alignment'][0],
                person = p['person'][0],
                number = p['number'][0],
                gender = gender,
                word=word,
                editor=editor
            )
            ptype.save()
            

    def backwards(self, orm):
        "Write your backwards methods here."

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'core.source': {
            'Meta': {'ordering': "['author', 'year']", 'object_name': 'Source', 'db_table': "'sources'", 'index_together': "[['author', 'year']]"},
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
        u'lexicon.lexicon': {
            'Meta': {'ordering': "['entry']", 'object_name': 'Lexicon', 'db_table': "'lexicon'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entry': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Language']"}),
            'loan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'loan_source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loan_source_set'", 'null': 'True', 'to': u"orm['core.Language']"}),
            'phon_entry': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
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
        u'pronouns.paradigm': {
            'Meta': {'object_name': 'Paradigm', 'db_table': "'paradigms'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'alignment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lexicon.Word']"})
        },
        u'pronouns.relationship': {
            'Meta': {'object_name': 'Relationship', 'db_table': "'pronoun_relationships'"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entry1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry1'", 'to': u"orm['lexicon.Lexicon']"}),
            'entry2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry2'", 'to': u"orm['lexicon.Lexicon']"}),
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

    complete_apps = ['auth', 'pronouns']
    symmetrical = True
