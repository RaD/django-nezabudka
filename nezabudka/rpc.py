from nezabudka.utils.extjs import RpcRouter
from nezabudka.models import Ticket
from django.conf import settings

class MainApiClass(object):
    
    def hello(self, name, user):
        return {
            'msg': 'Hello %s!' % name
        }
    
    hello._args_len = 1

class TicketApiClass(object):
    
    def read(self, rdata, user):
        start = int(rdata.get('start', 0))
        end = start + int(rdata.get('limit', settings.TICKETS_ON_PAGE))   
                
        qs = Ticket.objects.exclude(is_active=False)
        data = [item.store_record() for item in qs[start:end]]
        return {'data': data, 'count': qs.count()}        
    
    read._args_len = 1
    
class Router(RpcRouter):
    
    def __init__(self):
        self.url = 'nezabudka:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'TicketApi': TicketApiClass()
        }
        self.enable_buffer = 50
