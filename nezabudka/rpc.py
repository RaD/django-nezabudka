from nezabudka.utils.extjs import RpcRouter
from nezabudka.models import Project
from django.conf import settings

class MainApiClass(object):
    
    def hello(self, name, user):
        return {
            'msg': 'Hello %s!' % name
        }
    
    hello._args_len = 1

class ProjectApiClass(object):
    pass
    
class Router(RpcRouter):
    
    def __init__(self):
        self.url = 'nezabudka:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'ProjectApi': ProjectApiClass()
        }
        self.enable_buffer = 50
