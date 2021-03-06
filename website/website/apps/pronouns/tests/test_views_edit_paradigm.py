from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word
from website.apps.pronouns.tools import full_repr_row, short_repr_row
from website.apps.pronouns.models import Paradigm, PronounType


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


class Test_EditParadigmView(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Note, this requires the full pronoun complement."""
        cls.editor = User.objects.create_user(
            'admin', 'admin@admin.com', "test"
        )
        cls.lang = Language.objects.create(
            language='A',
            slug='langa',
            information='i.1',
            classification='a, b',
            isocode='aaa',
            editor=cls.editor
        )
        cls.source = Source.objects.create(
            year="1991",
            author='Smith',
            slug='Smith1991',
            reference='S2',
            comment='c1',
            editor=cls.editor
        )
        
        # Load all pronoun combinations
        for i, p in enumerate(PronounCombinations, 1):
            # create word
            w = short_repr_row(p)
            this_word = Word.objects.create(
                word=w,
                slug=w.lower().replace(" ", "_"),
                full=full_repr_row(p),
                editor=cls.editor
            )
            this_word.save()
            
            gender = p['gender'] if p['gender'] is None else p['gender'][0]
            
            ptype = PronounType.objects.create(
                alignment=p['alignment'][0],
                person=p['person'][0],
                number=p['number'][0],
                gender=gender,
                sequence=i,
                word=this_word,
                editor=cls.editor
            )
            ptype.save()
            
        # change the paradigm, man
        cls.fullpdm = Paradigm.objects.create(
            language=cls.lang,
            source=cls.source,
            editor=cls.editor,
            comment="full paradigm"
        )
        cls.fullpdm.save()
        
        # add some lexicon...
        for p in cls.fullpdm.pronoun_set.all():
            lex = Lexicon.objects.create(
                editor=cls.editor,
                language=cls.lang,
                source=cls.source,
                word=p.pronountype.word,
                entry='%d' % p.id
            )
            lex.save()
            p.entries.add(lex)
        
        cls.url = reverse(
            'pronouns:edit', kwargs={'paradigm_id': cls.fullpdm.id}
        )
        cls.detail_url = reverse(
            'pronouns:detail', kwargs={'paradigm_id': cls.fullpdm.id}
        )
    
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
    def _generate_post_data(self, paradigm):
        """Helper function to generate some post data"""
        postdata = {
            'submit': 'true',
            'pdm-language': u'%d' % self.lang.id,
            'pdm-source': u'%d' % self.source.id,
        }
        for pronoun in paradigm.pronoun_set.all():
            key = '%d_%d' % (pronoun.paradigm_id, pronoun.id)
            postdata['%s-TOTAL_FORMS' % key] = u'1'
            postdata['%s-INITIAL_FORMS' % key] = u'1'
            postdata['%s-MAX_NUM_FORMS' % key] = u'1000'
            
            for idx, entry in enumerate(pronoun.entries.all()):
                postdata['%s-%d-id' % (key, idx)] = u'%d' % entry.id
                postdata['%s-%d-entry' % (key, idx)] = entry.entry
                postdata['%s-%d-annotation' % (key, idx)] = entry.annotation
        return postdata
    
    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'pronouns/edit.html')
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_fail_when_not_logged_in(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=%s" % (reverse('login'), self.url)
        )
        
    def test_plumbing(self):
        """tests the internal plumbing of this test case."""
        for p in self.fullpdm.pronoun_set.all():
            assert p.entries.count() == 1
    
    def test_form_load(self):
        for formid, formdict in self.response.context['pronouns']:
            for alignment in ("A", "S", "O", "P"):
                assert alignment in formdict
                formset = formdict[alignment]
                assert len(formset.forms) == 1
                obj = formset.forms[0].instance
                # want to find pronoun type for this obj.
                pron = obj.pronoun_set.all()[0]
                assert full_repr_row(pron) == formid
                assert alignment == pron.pronountype.alignment
                
    def test_form_save(self):
        postdata = self._generate_post_data(self.fullpdm)
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, self.detail_url)
    
    def test_form_save_with_change(self):
        postdata = self._generate_post_data(self.fullpdm)
        # add 10000 to the id stored in -entry
        for p in postdata:
            if p.endswith('-entry'):
                postdata[p] = int(postdata[p]) + 10000
        
        response = self.client.post(self.url, postdata)
        self.assertRedirects(response, self.detail_url)
        
        updatedpdm = Paradigm.objects.get(pk=self.fullpdm.id)
        # find the updated lexical entries..
        for pronoun in updatedpdm.pronoun_set.all():
            assert pronoun.entries.count() == 1
            lex = pronoun.entries.all()[0]
            assert int(lex.entry) == (10000 + pronoun.id)
    
