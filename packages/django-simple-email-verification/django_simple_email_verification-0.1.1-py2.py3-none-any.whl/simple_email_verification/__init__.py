from django.conf import settings
"""
    Configuration options for the ``simple_email_verification`` package:

    All options reside in a dictionary, ``SIMPLE_EMAIL_VERIFICATION`` within your project's ``settings.py``. The options
    are as follows:

        VERIFICATION_FORM_TEMPLATE      Used for overriding the default verification form
        VERIFICATION_EMAIL_SUBJECT      Configures the Subject of the verification e-mail
        VERIFICATION_EMAIL_PLAINTEXT    Used for overriding the default plaintext e-mail template
        VERIFICATION_EMAIL_HTML         Used for overriding the default HTML e-mail template
        GET_TOKEN_PARAM_NAME            Name of the verification token when passed as a GET parameter
        SESSION_TOKEN_PARAM_NAME        Name of the verification token residing in the session
        EMAIL_ADDRESS_PARAM_NAME        Parameter name that contains the e-mail address when posted from the verification form
        EMAIL_FROM_ADDRESS              "From" e-mail address of verification e-mails

    To configure any or all of these options, you simply need to define them in ``settings.py``:

        SIMPLE_EMAIL_VERIFICATION = {
            'VERIFICATION_FORM_TEMPLATE': 'myapp/templates/my_custom_form.html',
            'EMAIL_ADDRESS_PARAM_NAME': 'my_custom_email_field',
            'EMAIL_FROM_ADDRESS': 'myaddress@mydomain.tld',
            ...
        }

"""

default_app_config = 'simple_email_verification.apps.SimpleEmailVerificationConfig'

def get_settings():
    """
        This function returns a dict containing default settings
    """
    s = getattr(settings, 'SIMPLE_EMAIL_VERIFICATION', {})
    s = {
            'VERIFICATION_FORM_TEMPLATE': s.get('VERIFICATION_FORM_TEMPLATE', 'simple_email_verification/verify.html'),
            'VERIFICATION_EMAIL_SUBJECT': s.get('VERIFICATION_EMAIL_SUBJECT', 'E-Mail Address Verification'),
            'VERIFICATION_EMAIL_PLAINTEXT': s.get(
                'VERIFICATION_EMAIL_PLAINTEXT', 'simple_email_verification/confirm.txt'),
            'VERIFICATION_EMAIL_HTML': s.get('VERIFICATION_EMAIL_HTML', 'simple_email_verification/confirm.html'),
            'GET_TOKEN_PARAM_NAME': s.get('GET_TOKEN_PARAM_NAME', 'get_verification'),
            'SESSION_TOKEN_PARAM_NAME': s.get('SESSION_TOKEN_PARAM_NAME', 'session_verification'),
            'EMAIL_ADDRESS_PARAM_NAME': s.get('EMAIL_ADDRESS_PARAM_NAME', 'email_address'),
            'EMAIL_FROM_ADDRESS': s.get('EMAIL_FROM_ADDRESS', 'donotreply@domain.tld'),
        }
    return s
