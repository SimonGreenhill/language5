
from fabric.api import local, require, run

def prod():
    """Set the target to production."""
    set(fab_hosts=['sjg.webfactional.com'])
    #set(fab_key_filename='/Users/sjl/.ssh/stevelosh')
    set(remote_root_dir='/home/sjg/webapps/transnewguinea')
    
    # where apache lives.
    set(remote_apache_dir='/home/sjg/webapps/transnewguinea/apache2')
    
    # top of the hg repository.
    set(remote_repository_dir='/home/sjg/webapps/transnewguinea/transnewguinea')

    # the dir with manage.py.
    set(remote_app_dir='/home/sjg/webapps/transnewguinea/transnewguinea/website')
 

def deploy():
    """Deploy the site."""
    require('fab_hosts', provided_by = [prod,])
    local("hg push")
    run("cd $(remote_repository_dir); hg pull; hg update")
    run("cd $(remote_app_dir); python2.7 manage.py syncdb")
    run("cd $(remote_app_dir); python2.7 manage.py migrate")
    run("cd $(remote_app_dir); pip install --upgrade -t ./lib -f ../transnewguinea/requirements.txt")
    run("$(remote_apache_dir)/bin/stop; sleep 1; $(remote_apache_dir)/bin/start")

def test(app=None):
    """Runs tests"""
    if app is not None:
        local("python manage.py test website.apps.%s" % app)
    else:
        local("python manage.py test")
        
        
def lint():
    """Runs pyflakes"""
    local("pyflakes .")
    
def py2to3():
    """Runs 2to3"""
    local("2to3 .")

def update():
    """Updates official bitbucket repo"""
    local("hg push")

