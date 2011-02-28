from django import forms
from nezabudka.models import Ticket

class CreateTicket(forms.ModelForm):
    
    class Meta:
        model = Ticket
