from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render
from smtplib import SMTPRecipientsRefused
from .send_confirmation import EmailMessage
from .models import VerifiedEmail
from .forms import *
from simple_email_verification import get_settings

s = get_settings()

def send_token_view(request):
    if request.method == 'POST':
        email = request.POST.get(s.get('EMAIL_ADDRESS_PARAM_NAME'), None)
        if email:
            instance, is_new = VerifiedEmail.objects.get_or_create(email_address=email)
            if not is_new:
                instance.update_token()
            verification_form = VerifiedEmailForm(request.POST, instance=instance)
            if verification_form.is_valid():
                verification_form.save()
                confirm_uri = request.build_absolute_uri(
                    '{0}?{1}={2}'.format(
                        request.path, s.get('GET_TOKEN_PARAM_NAME'), instance.verification_token))
                e = EmailMessage(confirm_uri=confirm_uri)
                try:
                    e.send(s.get('EMAIL_FROM_ADDRESS'), [instance.email_address])
                except SMTPRecipientsRefused as e:  # Create error handler for this.
                    messages.error(request, e.message)
                    raise PermissionDenied
                return render(request, s.get('VERIFICATION_FORM_TEMPLATE'))
    return None

