from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun
from website.apps.pronouns.tests import DefaultSettingsMixin
from website.apps.pronouns.forms import create_pronoun_formset
from website.apps.pronouns.forms import save_pronoun_formset
from website.apps.pronouns.forms import pronoun_formsets_are_valid
from website.apps.pronouns.forms import sort_formset


class FormsetSettingsMixin(object):
    """
    Extra Settings Mixin for Formsets Test
    
    Adds a `Lexicon` entry to each pronoun, with the `entry` and 
    `annotation` fields set to:
        entry = 'pron-%d' % pronoun.id
        annotation = 'ann-%d' % pronoun.id
    
    ...and adds the helper function `_generate_post_data` to fake up 
    some dummy POST data for a given `Paradigm` object.
    
    ...and the helper function `_add_extra_entry` which just creates
    another `Lexicon` entry to the first pronoun, with:
        entry = 'EXTRA'
        annotation = 'banana'
    
    """
    def setUp(self):
        self.add_fixtures()
        # add some entries and comments
        for pron in self.pdm.pronoun_set.all():
            # modify the stored entries so we can identify them later.
            pron.entries.add(Lexicon.objects.create(
                editor=self.editor, 
                source=self.source,
                language=self.lang,
                word=self.word,
                entry='pron-{0}'.format(pron.id),
                annotation='ann-{0}'.format(pron.id)
            ))
            pron.save()
    
    def _generate_post_data(self, paradigm):
        """Helper function to generate some post data"""
        postdata = {'submit': 'true'}
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
    
    def _add_extra_entry(self):
        # pick one pronoun to add an extra entry to.
        pron_with_extra = self.pdm.pronoun_set.all()[0]
        pron_with_extra.entries.add(Lexicon.objects.create(
            editor=self.editor, 
            source=self.source,
            language=self.lang,
            word=self.word,
            entry='EXTRA',
            annotation='banana'
        ))
        pron_with_extra.save()
        return pron_with_extra
    

class TestFormsetValidity(DefaultSettingsMixin, FormsetSettingsMixin, TestCase):
    def test_valid(self):
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        assert pronoun_formsets_are_valid(formsets)
    
    def test_add_valid(self):
        self._add_extra_entry()
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        assert pronoun_formsets_are_valid(formsets)
    
    def test_change_is_valid(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-0-entry'] = 'testing' # change something
        formsets = create_pronoun_formset(self.pdm, postdata)
        assert pronoun_formsets_are_valid(formsets)
    
    def test_is_valid_with_addition(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-1-entry'] = 'testing' # change something
        postdata['1_1-TOTAL_FORMS'] = u'2'
        formsets = create_pronoun_formset(self.pdm, postdata)
        assert pronoun_formsets_are_valid(formsets)


class TestFormsetCreator(DefaultSettingsMixin, FormsetSettingsMixin, TestCase):
    def test_all_forms_get_created(self):
        """Do we get the right number of forms?"""
        formsets = create_pronoun_formset(self.pdm)
        assert len(formsets) == self.pdm.pronoun_set.count()
    
    def test_all_forms_are_valid(self):
        """All created formsets with these data should be valid"""
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        for formid, formset in formsets:
            for form in formset.forms:
                if not form.is_valid():
                    raise AssertionError("Form should be valid. Errors are: %r" % form.errors)
            assert formset.is_valid(), "Formset should be valid. Errors are: %r" % formset.errors
            
    def test_each_formset_gets_the_right_entry(self):
        """Does each formset have the correct entry?"""
        formsets = create_pronoun_formset(self.pdm)
        for formid, form in formsets:
            assert len(form.forms) == formid.entries.count() == 1
            # is PK correct?
            assert form.forms[0].initial['entry'] == 'pron-%d' % formid.entries.all()[0].pk
    
    def test_each_formset_gets_the_right_values(self):
        """Is the value of each form field set correctly?"""
        formsets = create_pronoun_formset(self.pdm)
        for formid, form in formsets:
            assert len(form.forms) == formid.entries.count() == 1
            initial = form.forms[0].initial
            expected = formid.entries.all()[0]
            for key in initial:
                assert getattr(expected, key) == initial[key], \
                    'Expected %s to be %r not %r' % (key, expected, initial[key])
    
    def test_formset_with_multiple_entries(self):
        pron_with_extra = self._add_extra_entry()
        # test formset
        formsets = create_pronoun_formset(self.pdm)
        
        for formid, form in formsets:
            if formid == pron_with_extra:
                assert len(form.forms) == formid.entries.count() == 2
            else:
                assert len(form.forms) == formid.entries.count() == 1
    
    def test_formset_submssion(self):
        """Test POST data works"""
        postdata = self._generate_post_data(self.pdm)
        formsets = create_pronoun_formset(self.pdm, postdata)
        for formid, formset in formsets:
            assert not formset.has_changed()
    
    def test_formset_submission_with_update(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-0-entry'] = 'testing' # change something
        
        formsets = create_pronoun_formset(self.pdm, postdata)
        
        for f in formsets: 
            assert f[1].is_valid(), "Formset should be valid!"
            if f[0].id == 1:
                assert f[1].has_changed(), "This one formset should have changed!"
            else:
                assert not f[1].has_changed(), "This formset should not have changed!"
    
    def test_formset_submission_with_create(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-1-entry'] = 'testing' # change something
        postdata['1_1-TOTAL_FORMS'] = u'2'
        formsets = create_pronoun_formset(self.pdm, postdata)
        
        for f in formsets: 
            assert f[1].is_valid(), "Formset should be valid!"
            if f[0].id == 1:
                assert f[1].has_changed(), "This one formset should have changed!"
            else:
                assert not f[1].has_changed(), "This formset should not have changed!"
            
    def test_save(self):
        postdata = self._generate_post_data(self.pdm)
        
        for pronoun, formset in create_pronoun_formset(self.pdm, postdata):
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
        
        assert Lexicon.objects.count() == 3, "expecting 3"
        
    def test_save_with_update(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-0-entry'] = 'testing' # change something
        
        for pronoun, formset in create_pronoun_formset(self.pdm, postdata):
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
        
        # should still only have 3 lexical items
        assert Lexicon.objects.count() == 3, "expecting 3"
        
        # ...but the form of pk 1 should have changed..
        lex = Lexicon.objects.get(pk=1)
        assert lex.entry == 'testing'
        
    def test_save_with_addition(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-1-entry'] = 'testing' # change something
        postdata['1_1-TOTAL_FORMS'] = u'2'
        
        for pronoun, formset in create_pronoun_formset(self.pdm, postdata):
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
        
        # should now have 4 lexical items
        assert Lexicon.objects.count() == 4, "expecting 4"
        
        # CHECK VALUES....
        for pron in self.pdm.pronoun_set.all():
            entries = pron.entries.all().order_by('id')
            
            if pron.id == 1:
                assert len(entries) == 2
                assert entries[0].entry == 'pron-{0}'.format(pron.id)
                assert entries[0].annotation == 'ann-{0}'.format(pron.id)
                # the new lexical entry!
                assert entries[1].entry == 'testing'
                assert entries[1].annotation == ''
            else:
                assert len(entries) == 1
                assert entries[0].entry == 'pron-{0}'.format(pron.id)
                assert entries[0].annotation == 'ann-{0}'.format(pron.id)
                
    def test_repeated_saves_dont_explode(self):
        # saving the same data multiple times should not increase the size of the set.
        
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-1-entry'] = 'testing' # change something
        postdata['1_1-TOTAL_FORMS'] = u'2'
        
        for pronoun, formset in create_pronoun_formset(self.pdm, postdata):
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
        
        # should now have 4 lexical items
        assert Lexicon.objects.count() == 4, "expecting 4"
        
        # CHECK VALUES....
        for pron in self.pdm.pronoun_set.all():
            entries = pron.entries.all().order_by('id')
            
            if pron.id == 1:
                assert len(entries) == 2
                assert entries[0].entry == 'pron-{0}'.format(pron.id)
                assert entries[0].annotation == 'ann-{0}'.format(pron.id)
                # the new lexical entry!
                assert entries[1].entry == 'testing'
                assert entries[1].annotation == ''
            else:
                assert len(entries) == 1
                assert entries[0].entry == 'pron-{0}'.format(pron.id)
                assert entries[0].annotation == 'ann-{0}'.format(pron.id)
        
    def test_save_with_delete(self):
        postdata = self._generate_post_data(self.pdm)
        postdata['1_1-0-entry'] = u''
        
        for pronoun, formset in create_pronoun_formset(self.pdm, postdata):
            saved = save_pronoun_formset(self.pdm, pronoun, formset, self.editor)
            
        # should now have 2 lexical items
        assert Lexicon.objects.count() == 2, "expecting 2"
        # should have an empty pronoun set for pronoun 1
        assert Pronoun.objects.get(pk=1).entries.count() == 0
        # should have deleted the lexical object 1
        with self.assertRaises(Lexicon.DoesNotExist):
            assert Lexicon.objects.get(pk=1)
            


class TestFormsetSorter(DefaultSettingsMixin, FormsetSettingsMixin, TestCase):
    def test_number_of_rows(self):
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        sortf = sort_formset(formsets)
        assert len(sortf) == 3
    
    def test_tokens(self):
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        rows = sort_formset(formsets)
        assert rows[0][0] == u'1st (excl) Person Singular'
        assert rows[1][0] == u'2nd Person Singular'
        assert rows[2][0] == u'3rd Person Singular'
    
    def test_four_per_row(self):
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        for row in sort_formset(formsets):
            assert len(row[1]) == 4
            assert 'A' in row[1]
            assert 'S' in row[1]
            assert 'O' in row[1]
            assert 'P' in row[1]
    
    def test_row_formsets(self):
        formsets = create_pronoun_formset(self.pdm, self._generate_post_data(self.pdm))
        for row in sort_formset(formsets):
            assert row[1]['A'] is not None
            assert row[1]['S'] is None
            assert row[1]['O'] is None
            assert row[1]['P'] is None
        
        