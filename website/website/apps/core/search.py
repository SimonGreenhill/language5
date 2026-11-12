"""Site search: results grouped by type, exact matches first."""
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import render
from watson import search as watson

from website.apps.core.models import AlternateName, Family, Language, Source
from website.apps.lexicon.models import Lexicon, Word

# key, heading, queryset, field compared for exact matches, results shown in the "all" view
GROUPS = [
    ('languages', 'Languages', lambda: Language.objects.all(), 'language', 10),
    ('names', 'Alternate names', lambda: AlternateName.objects.select_related('language'), 'name', 5),
    ('families', 'Families', lambda: Family.objects.all(), 'family', 5),
    ('words', 'Words', lambda: Word.objects.all(), 'word', 10),
    ('sources', 'Sources', lambda: Source.objects.all(), 'author', 5),
    ('lexicon', 'Lexical items',
     lambda: Lexicon.objects.select_related('word', 'language', 'source'), 'entry', 20),
]
PER_PAGE = 50


def ranked(queryset, field, query):
    """watson full-text matches, exact (case-insensitive) matches on `field` first"""
    return watson.filter(queryset, query).annotate(
        exact=Case(When(**{f'{field}__iexact': query}, then=Value(0)), default=Value(1),
                   output_field=IntegerField())
    ).order_by('exact', '-watson_rank', 'pk')


def search(request):
    query = request.GET.get('q', '').strip()
    selected = request.GET.get('type')
    groups, page = [], None
    if query:
        for key, label, queryset, field, preview in GROUPS:
            results = ranked(queryset(), field, query)
            count = results.count()
            if not count:
                continue
            group = {'key': key, 'label': label, 'count': count, 'results': results[:preview],
                     'url': '?' + urlencode({'q': query, 'type': key})}
            if key == selected:
                page = Paginator(results, PER_PAGE).get_page(request.GET.get('page'))
                group['results'] = page.object_list
            groups.append(group)
    if selected not in {g['key'] for g in groups}:
        selected, page = None, None
    page_url = lambda n: '?' + urlencode({'q': query, 'type': selected, 'page': n})
    return render(request, 'core/search.html', {
        'query': query,
        'all_url': '?' + urlencode({'q': query}),
        'groups': [g for g in groups if not selected or g['key'] == selected],
        'tabs': groups,
        'total': sum(g['count'] for g in groups),
        'selected': selected,
        'page_obj': page,
        'prev_url': page_url(page.previous_page_number()) if page and page.has_previous() else None,
        'next_url': page_url(page.next_page_number()) if page and page.has_next() else None,
    })
