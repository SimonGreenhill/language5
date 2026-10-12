# Staging on Opalstack (`transnewguinea2`)

App: `~/apps/transnewguinea2`, Opalstack Django/uWSGI app, port 14764. `A=~/apps/transnewguinea2` below.

## 0. Before you start

- **Prod has uncommitted edits.** Live `robots.txt` (and, before its removal, the Twitter link) differ from every committed revision. In the prod checkout, run `hg status && hg diff` (or `git status && git diff`) and send me the output, so nothing is lost at cut-over.

## 1. Code

```
git clone -b modernise https://github.com/SimonGreenhill/language5.git $A/language5
```

## 2. Dependencies (env is Python 3.13.16, so Opalstack's uWSGI stays)

```
$A/env/bin/pip install -r $A/language5/requirements.txt
```
In `$A/uwsgi.ini`:
```
python-path = /home/sjg/apps/transnewguinea2/language5/website
wsgi-file = /home/sjg/apps/transnewguinea2/language5/website/website/wsgi.py
touch-reload = /home/sjg/apps/transnewguinea2/language5/website/website/wsgi.py
```

## 3. Database

Create a Postgres DB and user in the Opalstack panel (e.g. `sjg_tng2`). Also create an empty `sjg_tng2_test` with the same user: Opalstack users can't `CREATE DATABASE`, so tests reuse it via `--keepdb`. Restore a **fresh** prod dump:
```
pg_dump -Fc -U simon -h localhost sjg_tng > ~/tng-staging.dump
pg_restore --no-owner --no-acl -h localhost -U <dbuser> -d sjg_tng2 ~/tng-staging.dump
```

## 4. Static files

Create an "Nginx Static Only" app (e.g. `tng2_static`) and route it at `/static` on the staging site.

## 5. Settings

```
cp $A/language5/website/website/settings/local.template $A/language5/website/website/settings/local.py
```
Fill it in from prod's `local.py` (SITE_NAME, SITE_DESCRIPTION, OLAC, PIWIK_ID, EMAIL). Then set:
- `SECRET_KEY`: new: `$A/env/bin/python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"`
- `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS`: the staging domain
- `DATABASES`: `sjg_tng2` and its user/password
- `STATIC_ROOT = '/home/sjg/apps/tng2_static'`, `STATIC_URL = '/static/'`
- `MEDIA_ROOT = '/home/sjg/apps/transnewguinea2/media'` (staging uploads stay out of prod), `MEDIA_URL`: prod's, so existing attachments resolve
- `ADMINS`: your address
- `PIWIK_ID = ''` on staging, so test traffic isn't counted

## 6. Cut-over steps on the staging DB (same as prod later)

```
cd $A/language5/website
$A/env/bin/python manage.py check --deploy --fail-level WARNING
$A/env/bin/python manage.py migrate
psql -h localhost -U <dbuser> -d sjg_tng2 -f ../deploy/cutover.sql
$A/env/bin/python manage.py remove_stale_contenttypes --noinput
PGOPTIONS='-c statement_timeout=0' $A/env/bin/python manage.py buildwatson   # Opalstack's statement_timeout kills watson's cleanup DELETE
$A/env/bin/python manage.py collectstatic --noinput
$A/env/bin/python manage.py test --noinput --keepdb   # uses the pre-made test DB (see section 3)
$A/stop; sleep 2; $A/start
```

## 7. Verify

- Log in at `https://<staging>/accounts/login/`. **A CSRF 403 here means nginx isn't sending `X-Forwarded-Proto`.** Tell me, and I'll adjust `SECURE_PROXY_SSL_HEADER`.
- Check by hand: edit a lexicon entry, edit a word, run a cognacy save, quick data entry, and the admin history page.
- From any machine: `deploy/compare.py https://transnewguinea.org https://<staging>`. Expected differences: the canonical link, uncompressed CSS links, the Pronouns nav link gone, and `meta.next` parameter order.

Routine deploys after this: `$A/language5/deploy/deploy.sh`.
