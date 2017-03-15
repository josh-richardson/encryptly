from django.conf.urls import url
from django.http import HttpResponseRedirect

from encryptly_backend import views

# todo: fix this, categorize each webpage
urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('index')),
    url(r'^index/$', views.public.index, name='index'),
    url(r'^about/$', views.public.about, name='about'),
    url(r'^faq/$', views.public.faq, name='faq'),
    url(r'^contact/$', views.public.contact, name='contact'),

    url(r'^login/$', views.public.index, name='login'),
    url(r'^register/$', views.public.register, name='register'),


    url(r'^main/$', views.private.test_main, name='test_main'),

    url(r'^user/login/$', views.public.index, name='user_login'),



    url(r'^logout/$', views.public.index, name='logout'),
    url(r'^user/exists/$', views.api.user_exists, name='user_exists'),

]
