from django.conf.urls import url
from django.http import HttpResponseRedirect

from encryptly_backend import views

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('index')),
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact/$', views.index, name='contact'),

    url(r'^login/$', views.index, name='login'),
    url(r'^logout/$', views.index, name='logout'),
    url(r'^register/$', views.index, name='register'),

    url(r'^user/login/$', views.index, name='user_login'),

]
