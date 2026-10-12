#!/usr/bin/env python3
"""Compare anonymous pages and API output between two deployments.

Usage: deploy/compare.py https://transnewguinea.org https://staging.example.org
Both sites must serve the same data (staging restored from a fresh prod dump).
"""
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PATHS = [
    '/', '/about', '/language/', '/language/?page=2', '/language/?subset=A',
    '/source/', '/family/', '/word/', '/word/hand', '/cognacy/',
    '/language/kuman', '/source/abbott1985', '/family/amtomusan', '/iso/kue',
    '/search/?q=hand', '/robots.txt', '/statistics/', '/maps/language/',
    '/oai/?verb=Identify', '/oai/?verb=ListRecords&metadataPrefix=olac',
    '/api/v1/', '/api/v1/language/?limit=5', '/api/v1/language/abaga/',
    '/api/v1/word/?limit=5&offset=5', '/api/v1/lexicon/?language=1&limit=5',
    '/api/v1/source/?limit=2', '/api/v1/languagemap/?limit=2',
]

NOISE = [
    re.compile(r'name="csrfmiddlewaretoken" value="[^"]+"'),
    re.compile(r'<responseDate>[^<]+</responseDate>'),
    re.compile(r'\s+'),
]


def fetch(base, path, tries=4):
    req = urllib.request.Request(base + path, headers={'User-Agent': 'tng-compare'})
    opener = urllib.request.build_opener(NoRedirect)
    for attempt in range(tries):
        time.sleep(2 ** attempt)  # stay under Cloudflare's rate limit
        try:
            r = opener.open(req, timeout=60)
            return r.status, r.headers.get('Content-Type', ''), r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            if e.code != 429:
                return e.code, e.headers.get('Location', ''), ''
    return 429, '', ''


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def normalise(content_type, body):
    if 'json' in content_type:
        data = json.loads(body)
        meta = data.get('meta', {}) if isinstance(data, dict) else {}
        for key in ('next', 'previous'):
            if meta.get(key):  # tastypie versions order query params differently
                url = urllib.parse.urlsplit(meta[key])
                meta[key] = url.path + '?' + '&'.join(sorted(url.query.split('&')))
        return json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False)
    for pattern in NOISE:
        body = pattern.sub(' ', body)
    return body.replace('> <', '>\n<')


def main(old, new):
    same = 0
    for path in PATHS:
        a, b = fetch(old, path), fetch(new, path)
        if a[0] != b[0]:
            print(f'STATUS {path}: {a[0]} -> {b[0]} {b[1]}')
            continue
        x, y = normalise(a[1], a[2]), normalise(b[1], b[2])
        if x == y:
            same += 1
            continue
        diff = list(difflib.unified_diff(x.splitlines(), y.splitlines(), lineterm='', n=0))
        print(f'DIFF   {path}: {len(diff)} lines')
        print('\n'.join('    ' + line[:160] for line in diff[2:22]))
    print(f'{same}/{len(PATHS)} identical')


if __name__ == '__main__':
    main(*(u.rstrip('/') for u in sys.argv[1:3]))
