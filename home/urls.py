from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activationcodesending/$', views.sendActivationCode, name='sendcode'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm,name = 'confirm')
]