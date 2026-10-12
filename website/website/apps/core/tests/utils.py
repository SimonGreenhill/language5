class PaginatorTestMixin:
    """Mixin for running paginator tests. Needs self.url to be set."""
    def test_paginator(self):
        response = self.client.get(f'{self.url}?page=1')
        self.assertEqual(response.status_code, 200)
    
    def test_bad_paginator_integer(self):
        # no errors, just give page1
        response = self.client.get(f'{self.url}?page=10000')
        self.assertEqual(response.status_code, 404)
        
    def test_bad_paginator_word(self):
        response = self.client.get(f'{self.url}?page=banana')
        self.assertEqual(response.status_code, 404)
