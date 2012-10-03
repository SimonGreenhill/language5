
from fabric.api import local

def test():
    """Runs tests"""
    local("python manage.py test core olac")

def lint():
    """Runs pyflakes"""
    local("pyflakes .")
    
def py2to3():
    """Runs 2to3"""
    local("2to3 .")

def update():
    """Updates official bitbucket repo"""
    local("hg push")

