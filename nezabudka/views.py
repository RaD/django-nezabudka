from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def index(request):
    context = {
    }
    return direct_to_template(request, 'nezabudka/main/index.html', context)