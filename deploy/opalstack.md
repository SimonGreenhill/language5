# Staging on Opalstack (`transnewguinea2`)

App: `~/apps/transnewguinea2`, Opalstack Django/uWSGI app, port 14764. `A=~/apps/transnewguinea2` below.

## 0. Before you start

- **Prod has uncommitted edits.** Live `robots.txt` and the Twitter link differ from every committed revision. In the prod checkout, run `hg status && hg diff` (or `git status && git diff`) and send me the output, so nothing is lost at cut-over.
- Python: `$A/env/bin/python -V`. The port needs **≥ 3.11** (django-tables2 3.0). If it's 3.10, use 2b.

## 1. Code

```
git clone -b modernise https://github.com/SimonGreenhill/language5.git $A/language5
```

## 2a. Env is Python ≥ 3.11 (keep uWSGI)

```
$A/env/bin/pip install -r $A/language5/requirements.txt
```
In `$A/uwsgi.ini`:
```
python-path = /home/sjg/apps/transnewguinea2/language5/website
wsgi-file = /home/sjg/apps/transnewguinea2/language5/website/website/wsgi.py
touch-reload = /home/sjg/apps/transnewguinea2/language5/website/website/wsgi.py
```

## 2b. Env is Python 3.10 (switch to gunicorn on the same port)

uWSGI has no wheels for glibc 2.17, and compiling it isn't worth it. gunicorn is pure Python.
```
mv $A/env $A/env-uwsgi && python3.13 -m venv $A/env
$A/env/bin/pip install -r $A/language5/requirements.txt gunicorn
```
Replace `$A/start` (keep `$A/stop-uwsgi` as a backup of the old `stop`):
```
#!/bin/bash
A=/home/sjg/apps/transnewguinea2
mkdir -p $A/tmp; PIDFILE=$A/tmp/gunicorn.pid
if [ -e "$PIDFILE" ] && (pgrep -u sjg | grep -x -f $PIDFILE &> /dev/null); then exit 99; fi
cd $A/language5/website
$A/env/bin/gunicorn website.wsgi -w 3 -D -p $PIDFILE -b 127.0.0.1:14764 \
  --access-logfile /home/sjg/logs/apps/transnewguinea2/access.log \
  --error-logfile /home/sjg/logs/apps/transnewguinea2/error.log
```
`$A/stop`: `kill $(cat $A/tmp/gunicorn.pid) && rm $A/tmp/gunicorn.pid`. Opalstack's cron entry already calls `start`.
In `deploy/deploy.sh`, replace `touch website/wsgi.py` with `kill -HUP $(cat $APP/tmp/gunicorn.pid)`.

## 3. Database

Create a Postgres DB and user in the Opalstack panel (e.g. `sjg_tng2`). Restore a **fresh** prod dump:
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
$A/env/bin/python manage.py buildwatson
$A/env/bin/python manage.py collectstatic --noinput
$A/env/bin/python manage.py test --noinput   # needs CREATEDB on the db user; skip if not granted
$A/stop; sleep 2; $A/start
```

## 7. Verify

- Log in at `https://<staging>/accounts/login/`. **A CSRF 403 here means nginx isn't sending `X-Forwarded-Proto`.** Tell me, and I'll adjust `SECURE_PROXY_SSL_HEADER`.
- Check by hand: edit a lexicon entry, edit a word, run a cognacy save, quick data entry, and the admin history page.
- From any machine: `deploy/compare.py https://transnewguinea.org https://<staging>`. Expected differences: the canonical link, uncompressed CSS links, the Pronouns nav link gone, and `meta.next` parameter order.

Routine deploys after this: `$A/language5/deploy/deploy.sh`.
