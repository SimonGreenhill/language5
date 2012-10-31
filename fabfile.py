from fabric.api import env, run, local, require

STATICDIR = "website/static"


def prod():
    """Set the target to production."""
    env.hosts=['sjg@sjg.webfactional.com',]
    env.remote_root_dir='/home/sjg/webapps/transnewguinea'
    
    # where apache lives.
    env.remote_apache_dir='/home/sjg/webapps/transnewguinea/apache2'
    
    # top of the hg repository.
    env.remote_repository_dir='/home/sjg/webapps/transnewguinea/transnewguinea'

    # the dir with manage.py.
    env.remote_app_dir='/home/sjg/webapps/transnewguinea/transnewguinea/website'
    
    # virtualenv
    env.venv = 'transnewguinea'

def deploy():
    """Deploy the site."""
    require('hosts', provided_by = [prod,])
    run("cd %s; hg pull; hg update" % env.remote_repository_dir)
    # update site-packaged
    run("workon %s; cd %s; pip install --upgrade -t ./lib/ -r ./transnewguinea/requirements.txt" \
        % (env.venv, env.remote_root_dir))
    run("workon %s; cd %s; python2.7 manage.py syncdb" \
            % (env.venv, env.remote_app_dir))
    run("workon %s; cd %s; python2.7 manage.py migrate" % (env.venv,
                                                           env.remote_app_dir))
    # restart
    run("%s/bin/stop; sleep 1; %s/bin/start" % (env.remote_apache_dir,
                                                env.remote_apache_dir))

def update_assets():
    update_bootstrap()
    update_jquery()
    update_bootstrap_min_js()

def update_bootstrap():
    BSDIR = "thirdparty/bootstrap"
    local("cd %s; make clean; make bootstrap" % BSDIR)
    local("cp %s/bootstrap/css/bootstrap.min.css %s/css/bootstrap.min.css" %
          (BSDIR, STATICDIR))
    local("cp %s/bootstrap/css/bootstrap-responsive.min.css %s/css/bootstrap-responsive.min.css" %
          (BSDIR, STATICDIR))
    local("cp %s/bootstrap/img/* %s/img/" % (BSDIR, STATICDIR))

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

