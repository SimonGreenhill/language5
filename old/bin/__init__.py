import sys
import os

def bootstrap():
    """Bootstrap Django environment"""
    project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    project_name = os.path.basename(project_dir)
    sys.path.append(os.path.join(project_dir, '..'))
    sys.path.append("..")
    sys.path.pop()
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % project_name
    return
