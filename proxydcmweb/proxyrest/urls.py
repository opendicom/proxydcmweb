from django.conf.urls import url
from proxyrest import views

urlpatterns = [
    url(r'^session$', views.rest_login, name='login'),
    url(r'^session/(?P<session>[^/]+)/logout$', views.rest_logout, name='logout'),
]