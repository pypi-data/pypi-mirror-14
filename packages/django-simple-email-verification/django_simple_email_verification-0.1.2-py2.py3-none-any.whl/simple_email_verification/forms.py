from django.forms import ModelForm
from send_confirmation import EmailMessage
from .models import *

class VerifiedEmailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(VerifiedEmailForm, self).__init__(*args, **kwargs)
        self.send_token_on_save = kwargs.get('send_token_on_save', True)

    def save(self, *args, **kwargs):
        super(VerifiedEmailForm, self).save(*args, **kwargs)

    class Meta:
        model = VerifiedEmail
        fields = ('first_name', 'last_name', 'email_address')
