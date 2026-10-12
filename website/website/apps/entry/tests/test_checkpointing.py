

from website.apps.entry.models import Task
from website.apps.entry.views import encode_checkpoint, decode_checkpoint, make_querydict

from website.apps.entry.tests import DataMixin

class Test_Checkpointing(DataMixin):
    """Tests the Detail Page's Checkpointing"""
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # need an incomplete entry, or else we get marked as complete.
        del(cls.form_data['form-0-entry'])
    
    def test_checkpoint(self):
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            image=self.file_testimage,
            language=self.lang,
            done=False,
            checkpoint=encode_checkpoint(make_querydict(self.form_data)),
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        # get from db.
        t = Task.objects.get(pk=task.id)
        assert t.checkpoint is not None
        restored = decode_checkpoint(t.checkpoint)
        for k, v in self.form_data.items():
            assert k in restored, "Missing %s from checkpoint" % k
            assert restored[k] == v, f"Expected {k} to be {v}"
    
    def test_checkpoint_in_view(self):
        """Test checkpoint data goes through to view"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        
        del(self.form_data['form-0-language']) # make form invalid
        self.form_data['form-0-entry'] = 'banana'
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        
        # now check formdata in response
        formdata = [f.clean() for f in response.context['formset'].forms]
        assert 'entry' in formdata[0]
        assert formdata[0]['entry'] == 'banana'
        
    def test_no_checkpoint_on_GET(self):
        """GET shouldn't set checkpoint"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.get(self.task.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        assert self.task.checkpoint is None
        
    def test_checkpoint_on_POST(self):
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None
        
    def test_checkpoint_doesnt_override_better(self):
        """Don't restore a checkpoint if we've got a new one coming in via POST"""
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        # make sure the response has annotation = comment
        form = response.context['formset'].forms[0].data['form-0-annotation'] == 'comment'
        
        # make sure we've saved something...
        assert Task.objects.get(pk=self.task.id).checkpoint is not None
        
        # change the post data
        form_data = self.form_data.copy()
        form_data['form-0-annotation'] = 'TWO'
        response = self.client.post(self.task.get_absolute_url(), form_data)
        # Make sure - response contains annotation = 'TWO' not 'comment'
        form = response.context['formset'].forms[0].data['form-0-annotation'] == 'TWO'
        
    def test_checkpoint_with_unicode(self):
        unicode_sample = 'àáâãäåạɐæʌèéêëɛəìííîïɨịñŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·'
        retrieved = decode_checkpoint(encode_checkpoint(make_querydict({'entry': unicode_sample})))
        assert unicode_sample == retrieved['entry']
    
    def test_checkpoint_with_unicode_via_database(self):
        unicode_sample = 'àáâãäåạɐæʌèéêëɛəìííîïɨịñŋòóôõöøðɔþùúûüụųʔřɬɤƀꝑšʷᵘ·'
        task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            image=self.file_testimage,
            language=self.lang,
            done=False,
            checkpoint=encode_checkpoint(make_querydict({'entry': unicode_sample})),
            view="GenericView",
            records=1, # needed so we don't have too many empty forms to validate
        )
        assert unicode_sample == decode_checkpoint(Task.objects.get(pk=task.id).checkpoint)['entry']
    
    def test_refresh_sets_checkpoint(self):
        self.client.login(username="admin", password="test")
        assert self.task.checkpoint is None
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None



class Test_CheckpointFormat(DataMixin):
    """Checkpoints are JSON; pickles are never loaded."""

    def test_is_json(self):
        import json
        from django.http import QueryDict
        q = QueryDict('a=1&a=2&b=ŋ')
        encoded = encode_checkpoint(q)
        self.assertEqual(json.loads(encoded), {'a': ['1', '2'], 'b': ['ŋ']})
        restored = decode_checkpoint(encoded)
        self.assertEqual(restored.getlist('a'), ['1', '2'])
        self.assertEqual(restored['b'], 'ŋ')

    def test_pickle_not_loaded(self):
        import base64, pickle

        class Boom:
            def __reduce__(self):
                return (exec, ("raise SystemExit('unpickled')",))

        payload = base64.b64encode(pickle.dumps(Boom())).decode('ascii')
        self.assertIsNone(decode_checkpoint(payload))

    def test_migration_converts_legacy_pickle(self):
        import base64, importlib, pickle
        from django.http import QueryDict
        mig = importlib.import_module('website.apps.entry.migrations.0005_checkpoint_json')
        legacy = base64.b64encode(pickle.dumps(QueryDict('x=1&x=2&y=ŋ'), protocol=2)).decode('ascii')
        restored = decode_checkpoint(mig.pickle_to_json(legacy))
        self.assertEqual(restored.getlist('x'), ['1', '2'])
        self.assertEqual(restored['y'], 'ŋ')
        # and back, for rollback
        back = pickle.loads(base64.b64decode(mig.json_to_pickle(mig.pickle_to_json(legacy))))
        self.assertEqual(back.getlist('x'), ['1', '2'])

    def test_migration_loop_converts_and_reverts(self):
        import base64, importlib, pickle
        from django.apps import apps
        from django.http import QueryDict
        mig = importlib.import_module('website.apps.entry.migrations.0005_checkpoint_json')
        legacy = base64.b64encode(pickle.dumps(QueryDict('x=1&x=2'), protocol=2)).decode('ascii')
        task = Task.objects.create(
            editor=self.editor, name="T", description="", source=self.source,
            language=self.lang, view="GenericView", records=1, checkpoint=legacy,
        )
        mig.convert(apps, mig.pickle_to_json, legacy=True)
        task.refresh_from_db()
        self.assertEqual(decode_checkpoint(task.checkpoint).getlist('x'), ['1', '2'])
        mig.convert(apps, mig.pickle_to_json, legacy=True)  # idempotent
        mig.convert(apps, mig.json_to_pickle, legacy=False)
        task.refresh_from_db()
        self.assertEqual(pickle.loads(base64.b64decode(task.checkpoint)).getlist('x'), ['1', '2'])
