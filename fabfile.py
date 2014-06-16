import os
from fabric.api import env, run, local, require, get

STATICDIR = "website/static"

env.hosts=['sjg@simon.net.nz',]
env.remote_root_dir='/home/sjg/webapps/transnewguinea'
    
# where apache lives.
env.remote_apache_dir='/home/sjg/webapps/transnewguinea/apache2'
    
# top of the hg repository.
env.remote_repository_dir='/home/sjg/webapps/transnewguinea/transnewguinea'

# the dir with manage.py.
env.remote_app_dir='/home/sjg/webapps/transnewguinea/transnewguinea/website'
    
# virtualenv
env.venv = 'transnewguinea'

# things that dumpdata should ignore
dump_ignores = [
    'contenttypes', 
    'watson.searchentry', 
    'admin.logentry',
    'sessions.session', 
    'south.migrationhistory',
    'reversion.revision', 
    'reversion.version',
]






def deploy():
    """Deploy the site."""
    print '\nDEPLOY >> Updating remote mercurial repository...'
    update()
    print '\nDEPLOY >> Updating mercurial repository on deployment machine...'
    run("cd %s; hg pull; hg update" % env.remote_repository_dir)
    print '\nDEPLOY >> Syncing databases and migrating...'
    run("workon %s; cd %s; python2.7 manage.py syncdb" \
            % (env.venv, env.remote_app_dir))
    run("workon %s; cd %s; python2.7 manage.py migrate" % (env.venv,
                                                           env.remote_app_dir))
    print '\nDEPLOY >> Cleaning up...'
    run("cd %s; find . -name \*.pyc | xargs rm" % env.remote_repository_dir)
    run("workon %s; cd %s; python2.7 manage.py cleanup" % (env.venv,
                                                           env.remote_app_dir))
    print '\nDEPLOY >> Restarting Apache...'
    run("workon %s; %s/bin/restart" % (env.venv, env.remote_apache_dir))


def deploy_update_requirements():
    """Update site-packages using requirements file on deploy"""
    run("workon %s; cd %s; pip install --upgrade -r ./transnewguinea/requirements.txt" \
        % (env.venv, env.remote_root_dir))

def download_new_assets():
    """Update all assets"""
    update_jquery()
    update_bootstrap_min_js()

def make_bootstrap():
    """Makes bootstrap"""
    BSDIR = "thirdparty/bootstrap"
    local("cd %s; make clean; make bootstrap" % BSDIR)
    local("cp %s/bootstrap/css/bootstrap.min.css %s/css/bootstrap.min.css" %
          (BSDIR, STATICDIR))
    local("cp %s/bootstrap/css/bootstrap-responsive.min.css %s/css/bootstrap-responsive.min.css" %
          (BSDIR, STATICDIR))
    local("cp %s/bootstrap/img/* %s/img/" % (BSDIR, STATICDIR))
    local("cp %s/bootstrap/js/bootstrap.min.js %s/js/bootstrap.min.js" % (BSDIR, STATICDIR))

def update_jquery():
    url = "http://code.jquery.com/jquery-1.8.2.min.js"
    local("curl %s -o %s/js/jquery.js" % (url, STATICDIR))

def update_bootstrap_min_js():
    url = "https://raw.github.com/twitter/bootstrap/gh-pages/assets/js/bootstrap.min.js"
    local("curl %s -o %s/js/bootstrap.min.js" % (url, STATICDIR))

def test(app=None):
    """Runs tests"""
    if app is not None:
        local("cd website; python manage.py test website.apps.%s" % app)
    else:
        local("cd website; python manage.py test")
        
def lint():
    """Runs pyflakes"""
    local("cd website; pyflakes .")
    
def py2to3():
    """Runs 2to3"""
    local("cd website; 2to3 .")

def update():
    """Updates official bitbucket repo"""
    local("hg push")

def snapshot():
    """Takes a snapshot"""
    ignore = " ".join(['-e %s' % i for i in dump_ignores])
    run("workon %s; cd %s; python manage.py dumpdata --indent=2 %s > %s/dump.json" \
        % (env.venv, env.remote_app_dir, ignore, env.remote_root_dir))
    run("cd %s; gzip -9 -f dump.json" % env.remote_root_dir)
    get("%s/dump.json.gz" % env.remote_root_dir, "dump.json.gz")

def clone():
    """Clones the production database"""
    if os.path.isfile('dump.json.gz'):
        print("Using cached dump file at dump.json.gz -- remove to clone")
    else:
        snapshot()
    
    local("gunzip dump.json.gz")
    print("moving database.db to database.db-old")
    local("mv website/website/database.db website/website/database.db-old")
    local("cd website; python manage.py syncdb")
    local("cd website; python manage.py migrate --noinput")
    local("cd website; python manage.py loaddata ../dump.json")
    local("cd website; python manage.py createcachetable cache")
    local("gzip -9 dump.json") # recompress to keep cached
