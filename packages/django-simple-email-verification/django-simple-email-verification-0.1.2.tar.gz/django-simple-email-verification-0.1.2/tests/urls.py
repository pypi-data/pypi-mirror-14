from django.conf.urls import url
from .views import testview


urlpatterns = [ 
    url(r'^test/', testview),
]
