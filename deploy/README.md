# Crawler-trap fix — deployment guide

Closes the `?sort=` × `?page=` crawler trap that was saturating the app server
(`127.0.0.1:3298`). See `fix.md` and `.tmp/crawler-trap-fix.md` for the full
diagnosis and the list of files changed.

The fix has two halves:

| Half | Where | Status |
|------|-------|--------|
| **App code** (robots.txt, canonical/noindex, sort/page validation) | this repo | ✅ implemented — deploy with the app |
| **Edge** (rate-limit + micro-cache, or Cloudflare WAF) | server / Cloudflare | 📄 provided here as config — operator must apply |

## Deploy order (do 1–2 first; they are low-risk and stop most of the load)

### 1. Ship the app changes
Deploy the updated code as usual, then run the test suite on a host with the
app's virtualenv (Django 1.11 / Python 2.7):

```
./manage.py test website.apps.core website.apps.lexicon website.apps.cognacy
```

> These tests were written to the project conventions but could **not** be run
> in the authoring checkout (no Django 1.11 runtime there). Run them before
> rolling out.

**Verify live:**
- `curl -s https://transnewguinea.org/robots.txt` shows the new
  `Disallow: /*?*sort=` / `Disallow: /*?*page=` / `Crawl-delay: 10` lines.
- `curl -sI 'https://transnewguinea.org/language/?sort=sausage'` → `301` to
  `/language/` (invalid sort collapses to canonical).
- `curl -sI 'https://transnewguinea.org/language/?page=banana'` → `404`.
- View source of `https://transnewguinea.org/language/?sort=language` → contains
  `<meta name="robots" content="noindex,follow">` and a `<link rel="canonical">`
  pointing at the clean URL.

### 2. Cloudflare WAF (preferred edge mitigation)
Follow `cloudflare-waf-notes.md`. This is the best stop for the fake-`Chrome/145`
swarm because it challenges them without touching the origin. Roll out in
**challenge** mode, watch Security → Events, then tighten.

### 3. nginx rate-limit + micro-cache (origin protection / CF fallback)
Apply `nginx-crawler-trap.conf`. Add the `http{}` directives, then the
micro-cache on the list locations, then the `limit_req` **log-only first**.
Reload nginx: `nginx -t && systemctl reload nginx`.

## Canonical URL scheme (one-line settings check)
The `<link rel="canonical">` is built from the request scheme. This project does
**not** set `SECURE_PROXY_SSL_HEADER`, so if nginx terminates TLS and proxies to
the app over http, Django sees `http` and will emit an `http://…` canonical. If
the site is served over https, add to nginx (`proxy_set_header X-Forwarded-Proto
$scheme;`) **and** to Django settings:
```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```
so canonicals point at the https URL. (Not blocking — `noindex` is the primary
signal for the sort/page duplicates; canonical is secondary.)

## DB indexes (fix.md step 3, last bullet)
Make sure the columns real users sort by are indexed so legitimate sorts stay
cheap. The sort columns exposed on the list tables are (django-tables2 order
tokens): `language`, `isocode`, `classification`, `count`, `author`, `year`,
`reference`, `family`. Check the current schema and add indexes where missing,
e.g. for the Language/Source list ordering:

```sql
-- inspect first
\d+ core_language
\d+ core_source
-- add where a sort column is unindexed, e.g.:
CREATE INDEX IF NOT EXISTS core_language_language_idx ON core_language (language);
CREATE INDEX IF NOT EXISTS core_source_author_idx     ON core_source   (author);
```

`count` is a runtime aggregate (`COUNT(lexicon)`), not a column — it can't be
indexed directly; the micro-cache (step 3) is what absorbs those.

## Rollback
- App: redeploy the previous revision (all changes are additive; the new
  `crawler_trap.py` is only referenced by the list views).
- nginx: comment out the added directives and reload.
- Cloudflare: disable the WAF/Bot rules from the dashboard (instant).

## Out of scope (flag to the owner, separately)
CMS exploit probes in the logs (`com_sppagebuilder…uploadCustomIcon`,
`wp-admin…updraft_central`) — not causing the outages, but worth forwarding.
