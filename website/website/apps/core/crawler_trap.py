"""
Crawler-trap mitigation for django-tables2 list pages.

Bots enumerate a near-infinite ``?sort=`` x ``?page=`` URL space on the list
pages, each request triggering an expensive DB query. This module closes that
space at the application layer:

* ``guard_page``    -- reject bogus ``?page=`` values cheaply, before the DB.
* ``canonical_sort_redirect`` -- 301 any unknown ``?sort=`` value to the clean
  URL, collapsing the ``?sort=<junk>`` space into a single canonical page.
* ``list_seo_context`` -- ``<link rel=canonical>`` / ``<meta robots noindex>``
  context so search engines stop indexing the sort/page permutations.
* ``CrawlerTrapMixin`` -- wires the above into ``SingleTableView`` index views.

See ``fix.md`` / ``.tmp/crawler-trap-fix.md``.
"""
from django.http import Http404, HttpResponsePermanentRedirect

# No legitimate list on this site is anywhere near this many pages (bots ask for
# things like page=250 or page=2147483647). Real out-of-range pages are still
# 404'd by the Paginator; this is just a cheap early-out for absurd values.
MAX_PAGE = 10000


def valid_sort_columns(table_class):
    """Return the set of orderable column names for a django-tables2 table."""
    table = table_class([])
    return {
        bound_column.name
        for bound_column in table.columns
        if bound_column.orderable
    }


def canonical_sort_redirect(request, table_class):
    """
    If the request carries a ``?sort=`` value that is not a real, orderable
    column, return an ``HttpResponsePermanentRedirect`` to the same URL with
    ``sort`` removed (other params preserved). Returns ``None`` when ``sort`` is
    absent or valid, so callers can fall through to normal handling.

    django-tables2 accepts comma-separated multi-column sorts and a leading
    ``-`` for descending, so each token is validated independently.
    """
    raw = request.GET.get('sort')
    if not raw:
        return None

    allowed = valid_sort_columns(table_class)
    tokens = [token.lstrip('-') for token in raw.split(',') if token]
    if tokens and all(token in allowed for token in tokens):
        return None  # every requested column is real -- let it through

    params = request.GET.copy()
    del params['sort']
    querystring = params.urlencode()
    target = request.path + (('?' + querystring) if querystring else '')
    return HttpResponsePermanentRedirect(target)


def guard_page(request):
    """
    Reject obviously-bogus ``?page=`` values with ``Http404`` before any DB
    query runs. Genuine out-of-range pages are still handled downstream by the
    Paginator (``EmptyPage`` -> 404).
    """
    raw = request.GET.get('page')
    if raw is None:
        return
    try:
        page = int(raw)
    except (TypeError, ValueError):
        raise Http404
    if page < 1 or page > MAX_PAGE:
        raise Http404


def list_seo_context(request):
    """
    Context for ``base.html`` so list pages self-canonicalize:

    * ``canonical_url`` -- absolute URL with ``sort`` and ``page`` stripped
      (``subset`` and any other real filters are preserved).
    * ``noindex`` -- ``True`` when a ``sort`` is present or ``page`` > 1, i.e.
      when the page is a duplicate view of the canonical list.
    """
    params = request.GET.copy()
    for key in ('sort', 'page'):
        params.pop(key, None)
    querystring = params.urlencode()
    canonical = request.build_absolute_uri(request.path)
    if querystring:
        canonical = f'{canonical}?{querystring}'

    noindex = ('sort' in request.GET) or (
        request.GET.get('page', '1') not in ('', '1')
    )
    return {'canonical_url': canonical, 'noindex': noindex}


class CrawlerTrapMixin:
    """
    Mixin for ``SingleTableView`` index views. Validates ``?sort=``/``?page=``
    before the (expensive) queryset is built, and injects self-canonicalizing
    SEO context. Requires ``self.table_class`` (set on all the index views).
    """

    def get(self, request, *args, **kwargs):
        redirect = canonical_sort_redirect(request, self.table_class)
        if redirect is not None:
            return redirect
        guard_page(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(list_seo_context(self.request))
        return context
