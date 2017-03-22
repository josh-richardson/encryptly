from django.conf.urls import url

import chat
from chat import views

urlpatterns = [

    url(r'^index/', views.index, name="index"),
    url(r'^register/', views.register, name="register"),
    url(r'^login/', views.log_in, name="login"),
    # url(r'^add_contact/', views.add_contact, name="login")

]