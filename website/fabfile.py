
from fabric.api import local

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

