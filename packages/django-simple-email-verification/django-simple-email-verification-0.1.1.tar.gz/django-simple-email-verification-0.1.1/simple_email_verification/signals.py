import django.dispatch

address_verified = django.dispatch.Signal(providing_args=['instance'])

