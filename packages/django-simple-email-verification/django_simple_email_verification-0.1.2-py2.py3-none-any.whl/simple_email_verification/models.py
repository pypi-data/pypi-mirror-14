from django.db import models
from datetime import datetime
import uuid

def create_verification_token():
    return uuid.uuid4().hex


class VerifiedEmail(models.Model):

    first_name = models.CharField(max_length=40, null=True, blank=True)

    last_name = models.CharField(max_length=100, null=True, blank=True)

    email_address = models.EmailField(unique=True)

    verification_token = models.TextField(default=create_verification_token)

    created = models.DateTimeField(auto_now_add=True)

    last_verified = models.DateTimeField(null=True, blank=True)

    def update_last_verified(self, timestamp=datetime.now()):
        self.last_verified = timestamp
        self.save()
   
    def update_token(self):
        self.verification_token = create_verification_token()
        self.save()
        return self.verification_token

    def __unicode__(self):
        status = 'Pending' if self.last_verified == None else 'Verfied'
        if self.first_name and self.last_name:
            name = '{0} {1}, '.format(self.first_name, self.last_name)
        else:
            name = ''
        return "{0}<{1}>, Status: {2}".format(name, self.email_address, status)

    class Meta:
        verbose_name = "Verified E-Mail Address"
        verbose_name_plural = '{0}es'.format(verbose_name)
