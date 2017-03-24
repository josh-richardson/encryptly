from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static

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

	url(r'^profile/$', views.private.edit_profile, name='profile'),
	url(r'^delete/$', views.private.delete_profile, name="delete_profile"),
#	url(r'^profile/edit/$', views.private.edit_profile, name='edit_profile'),
    url(r'^main/$', views.private.test_main, name='test_main'),

    url(r'^settheme/([0-9])/$', views.private.set_theme, name='set_theme'),


    url(r'^user/logout/$', views.private.user_logout, name='logout'),

    url(r'^user/exists/$', views.api.user_exists, name='user_exists'),
    url(r'^user/login/$', views.api. user_login, name='user_login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
