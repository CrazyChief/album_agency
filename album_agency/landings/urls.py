from django.conf.urls import url
from .views import LandingView

app_name = 'landings'
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)([/]+|([^.*/]+))$', 
        LandingView.as_view(), name='land_view')
]
