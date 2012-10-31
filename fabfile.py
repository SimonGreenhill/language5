from fabric.api import env, run, local, require


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

