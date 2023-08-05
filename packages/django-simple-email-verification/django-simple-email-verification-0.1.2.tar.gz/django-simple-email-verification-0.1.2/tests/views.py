import json
from simple_email_verification.decorators import require_verification_token
from django.http import HttpResponse


@require_verification_token
def testview(request):
    response_data = {'response_data': 'email address verified'}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
