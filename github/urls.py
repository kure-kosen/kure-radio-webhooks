from django.conf.urls import url

from . import views

app_name = 'github'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^callback/$', views.callback, name='callback'),
]
