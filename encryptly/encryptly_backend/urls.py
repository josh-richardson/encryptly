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

    url(r'^login/$', views.public.login, name='login'),
    url(r'^register/$', views.public.register, name='register'),


    url(r'^main/$', views.private.test_main, name='test_main'),
    url(r'^themes/$', views.private.test_themes, name='test_themes'),
    url(r'^user/logout/$', views.private.user_logout, name='logout'),

    url(r'^user/exists/$', views.api.user_exists, name='user_exists'),
    url(r'^user/login/$', views.api. user_login, name='user_login'),


]
