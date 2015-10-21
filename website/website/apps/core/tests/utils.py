

class PaginatorTestMixin(object):
    """Mixin for running paginator tests. Needs self.url to be set."""
    def test_paginator(self):
        response = self.client.get('{}?page=1'.format(self.url))
        self.assertEqual(response.status_code, 200)
    
    def test_bad_paginator_integer(self):
        # no errors, just give page1
        response = self.client.get('{}?page=10000'.format(self.url))
        self.assertEqual(response.status_code, 404)
        
    def test_bad_paginator_word(self):
        response = self.client.get('{}?page=banana'.format(self.url))
        self.assertEqual(response.status_code, 404)
