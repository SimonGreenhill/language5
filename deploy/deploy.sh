#!/bin/bash
# Routine deploy on Opalstack. Usage: deploy/deploy.sh [appdir]
set -euo pipefail
APP=${1:-$HOME/apps/transnewguinea2}
PY=$APP/env/bin/python
cd "$APP/language5"
git pull --ff-only
"$APP/env/bin/pip" install -q -r requirements.txt
cd website
"$PY" manage.py check --deploy --fail-level WARNING
"$PY" manage.py migrate --noinput
"$PY" manage.py collectstatic --noinput -v0
touch website/wsgi.py   # uWSGI touch-reload restarts the workers
echo "Deployed $(git rev-parse --short HEAD)"
