from django.conf.urls import url

from . import views

app_name = 'tours'

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^create/$', views.TourCreate.as_view(), name='tour_form')
]
