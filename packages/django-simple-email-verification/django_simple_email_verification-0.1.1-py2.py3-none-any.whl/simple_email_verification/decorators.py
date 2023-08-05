from django.shortcuts import render, redirect
from .signals import address_verified
from .views import send_token_view
from .models import VerifiedEmail
from .forms import VerifiedEmailForm
from simple_email_verification import get_settings

s = get_settings()


def require_verification_token(view_func):
    def verify(request, *args, **kwargs):
        response = send_token_view(request)
        token = request.GET.get(s.get('GET_TOKEN_PARAM_NAME'))
        if token:
            try:
                v = VerifiedEmail.objects.get(verification_token=token)
            except VerifiedEmail.DoesNotExist:
                # Bad token! Make them re-verify.
                pass
            else:
                v.update_last_verified()
                address_verified.send(sender=__name__, instance=v)
                # Ensure that tokens can only be used once and that once a session expires the user must re-verify their
                # e-mail address. This prevents a malicious user from gaining access to a previously used verification
                # link and using it impersonate a previously verified e-mail address.
                request.session[s.get('SESSION_TOKEN_PARAM_NAME')] = v.update_token()
                response = redirect(request.path, context=request)
        else:
            token = request.session.get(s.get('SESSION_TOKEN_PARAM_NAME'))
            if token:
                try:
                    VerifiedEmail.objects.get(verification_token=token)
                    return view_func(request, *args, **kwargs)
                except VerifiedEmail.DoesNotExist:
                    pass
        if response:
            return response
        else:
            verification_form = VerifiedEmailForm()
            return render(request, s.get('VERIFICATION_FORM_TEMPLATE'), {'form': verification_form.as_p()})

    return verify
