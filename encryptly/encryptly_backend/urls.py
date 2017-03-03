from django.conf.urls import url

from encryptly_backend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]