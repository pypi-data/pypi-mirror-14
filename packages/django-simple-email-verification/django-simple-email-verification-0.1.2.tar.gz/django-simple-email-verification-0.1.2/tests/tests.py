from django.test import TestCase, Client
from simple_email_verification.models import VerifiedEmail
from simple_email_verification import get_settings

class EmailVerificationTestCase(TestCase):

    def setUp(self):
        self.settings = get_settings()
        self.email_param = self.settings.get('EMAIL_ADDRESS_PARAM_NAME')
        self.token_get_param = self.settings.get('GET_TOKEN_PARAM_NAME')
        self.token_session_param = self.settings.get('SESSION_TOKEN_PARAM_NAME')
        self.client = Client()

    def test_verification_request(self):
        # Visiting the decorated view without having first verified an e-mail
        # address, will result in an e-mail verification form being returned
        self.client.post('/test/', {
            self.email_param: 'user@domain.tld'})
        # Session token doesn't exist until *after* user has clicked
        # the verification link which has been sent to their e-mail
        self.assertEqual(self.client.session.get(self.token_session_param), None)
        v = VerifiedEmail.objects.get(email_address='user@domain.tld')
        # This simulates the user clicking the verification link
        self.client.get('/test/?{0}={1}'.format(self.token_get_param, v.verification_token))
        # Session token should exist now and it should be different from the token in the verification URL
        self.assertNotEquals(self.client.session.get(self.token_session_param), v.verification_token)
        # User has verified their e-mail so now they'll see the resulted of the decorated view
        self.assertEqual(self.client.get('/test/').json().get('response_data'), 'email address verified')
