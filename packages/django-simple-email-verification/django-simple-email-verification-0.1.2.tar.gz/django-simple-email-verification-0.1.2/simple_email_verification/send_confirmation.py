from socket import gaierror
from django.core.mail import send_mail
from django.template.loader import render_to_string
from simple_email_verification import get_settings

s = get_settings()


class EmailMessage:

    def __init__(self, **kwargs):
        self.subject = s.get('VERIFICATION_EMAIL_SUBJECT')
        self.plain = render_to_string(s.get('VERIFICATION_EMAIL_PLAINTEXT'), kwargs)
        self.html = render_to_string(s.get('VERIFICATION_EMAIL_HTML'), kwargs)

    def send(self, sender, recipients):
        try:
            send_mail(self.subject, self.plain, sender, recipients, html_message=self.html)
        except gaierror as e:
            # gaierror raised if SMTP hostname does not resolve or is incorrect.
            # Might like to include a more helpful error message and/or ... something.
            return e
